import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

BOTH_NOT_MUTATED = (1 - PROBS["mutation"]) * (1 - PROBS["mutation"])
BOTH_MUTATED = PROBS["mutation"] * PROBS["mutation"]
EXACTLY_ONE_MUTATED = (1 - PROBS["mutation"]) * PROBS["mutation"]

def get_prob_two_genes(m_gene, f_gene):
    if m_gene + f_gene == 4:
        return BOTH_NOT_MUTATED
    elif m_gene + f_gene == 3:
        return 0.5 * BOTH_NOT_MUTATED + 0.5 * EXACTLY_ONE_MUTATED
    elif m_gene + f_gene == 1:
        return 0.5 * EXACTLY_ONE_MUTATED
    elif m_gene + f_gene == 0:
        return BOTH_MUTATED
    elif m_gene == f_gene == 1:
        return 0.5 * 0.5 * (BOTH_NOT_MUTATED + BOTH_MUTATED + 2 * EXACTLY_ONE_MUTATED)
    else:
        return EXACTLY_ONE_MUTATED
    
def get_prob_one_gene(m_gene, f_gene):
    if m_gene + f_gene == 4:
        return EXACTLY_ONE_MUTATED
    elif m_gene + f_gene == 3:
        return 0.5 * (BOTH_NOT_MUTATED + BOTH_MUTATED) + 0.5 * EXACTLY_ONE_MUTATED
    elif m_gene + f_gene == 1:
        return 0.5 * (BOTH_NOT_MUTATED + BOTH_MUTATED) + 0.5 * EXACTLY_ONE_MUTATED
    elif m_gene + f_gene == 0:
        return EXACTLY_ONE_MUTATED
    elif m_gene == f_gene == 1:
        return 0.5 * 0.5 * (2 * (EXACTLY_ONE_MUTATED) + 2 * (BOTH_NOT_MUTATED + BOTH_MUTATED))
    else:
        return BOTH_NOT_MUTATED + BOTH_MUTATED

def get_prob_no_gene(m_gene, f_gene):
    if m_gene + f_gene == 4:
        return BOTH_MUTATED
    elif m_gene + f_gene == 3:
        return 0.5 * BOTH_MUTATED + 0.5 * EXACTLY_ONE_MUTATED
    elif m_gene + f_gene == 1:
        return 0.5 * BOTH_NOT_MUTATED + 0.5 * EXACTLY_ONE_MUTATED
    elif m_gene + f_gene == 0:
        return BOTH_NOT_MUTATED
    elif m_gene == f_gene == 1:
        return 0.5 * 0.5 * (BOTH_NOT_MUTATED + 2 * EXACTLY_ONE_MUTATED + BOTH_MUTATED)
    else:
        return EXACTLY_ONE_MUTATED

def create_person_info(people, one_gene, two_genes, have_trait):
    person_gene_trait = people.copy()

    for person in person_gene_trait:
        person_gene_trait[person] = {'gene': 0, 'trait': False}

    for person in one_gene:
        person_gene_trait[person]['gene'] = 1
    
    for person in two_genes:
        person_gene_trait[person]['gene'] = 2

    for person in have_trait:
        person_gene_trait[person]['trait'] = True
    
    return person_gene_trait


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    ans = 1
    
    no_gene = people.keys() - one_gene - two_genes

    person_info = create_person_info(people, one_gene, two_genes, have_trait)

    for person in two_genes:
        prob_two_gene = PROBS["gene"][2]
        mother = people[person]['mother']
        father = people[person]['father']
        if mother is not None and father is not None:
            prob_two_gene = get_prob_two_genes(person_info[mother]['gene'], 
                                               person_info[father]['gene'])
        ans *= prob_two_gene * PROBS["trait"][2][person_info[person]['trait']]

    for person in one_gene:
        prob_one_gene = PROBS["gene"][1]
        mother = people[person]['mother']
        father = people[person]['father']
        if mother is not None and father is not None:
            prob_one_gene = get_prob_one_gene(person_info[mother]['gene'], 
                                               person_info[father]['gene'])
        ans *= prob_one_gene * PROBS["trait"][1][person_info[person]['trait']] 

    for person in no_gene:
        prob_no_gene = PROBS["gene"][0]
        mother = people[person]['mother']
        father = people[person]['father']
        if mother is not None and father is not None:
            prob_no_gene = get_prob_no_gene(person_info[mother]['gene'], 
                                               person_info[father]['gene'])
        ans *= prob_no_gene * PROBS["trait"][0][person_info[person]['trait']]  

    return ans


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    no_gene = probabilities.keys() - one_gene - two_genes

    person_info = create_person_info(probabilities, one_gene, two_genes, have_trait)    
    
    for person in two_genes:
        probabilities[person]['gene'][2] += p
        probabilities[person]['trait'][person_info[person]['trait']] += p
    for person in one_gene:
        probabilities[person]['gene'][1] += p
        probabilities[person]['trait'][person_info[person]['trait']] += p
    for person in no_gene:
        probabilities[person]['gene'][0] += p
        probabilities[person]['trait'][person_info[person]['trait']] += p
    return


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for distribution in probabilities[person]:
            distribution = probabilities[person][distribution]
            total = sum(distribution.values())
            for key in distribution.keys():
                distribution[key] = distribution[key] / total
                
if __name__ == "__main__":
    main()
