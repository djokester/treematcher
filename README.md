# TreeMatcher: A new tool for creating Python-based queries on trees

### Program Description

In mathematics, a standard way of representing graphical trees with edge lengths is the Newick format. The TreeMatcher module extends the Newick format to define a tree pattern and includes rules and filters with a Python-based vocabulary. These patterns are then searched for using a tree traversal algorithm. A pattern can be written by accessing the attributes and functions available to an ETE Tree (see Tree and PhyloTree classes), using Python code directly, or through custom functions and syntax.

### How to use treematcher

The simplest way to begin using treematcher is to create a pattern on a single node. In the following example, a string defines the pattern and a TreePattern instance is created. If an attribute is not specified, the node name is assumed by default.

```
# Example 1: Find a node named "sample_1"
pattern1 = ' sample_1 ; '	 # begin with a string
pattern1 = TreePattern(pattern1)  # create a TreePattern Instance

```
Now that you know how to search for the name of a single node, you may be tempted to access other nodes through constraints like @.children[0].name=="sample_1" and @.children[1].name=="sample_2" but calling a node's descendants in this way restricts the order in which they are considered a match. For example, the permutation @.children[0].name=="sample_2" and @.children[1].name=="sample_1" would not be returned as a match. Using the Newick format ensures that both permutations of children are matched.

```
# Example 2: Find a tree where sample_1 and sample_2 are siblings.
pattern2 = TreePattern(' (sample_1, sample_2) ; ')
```

Note that the format type is set to 1 as the default which does not allow internal node names. Access other Newick format types using the format argument.

###
```
# Example 3: Find a tree where sample_1 and sample_2 are children of the parent ancestor_a.
pattern3 = ' (sample_1, sample_2) ancestor_a ; '
pattern3 = TreePattern(pattern3, format=8)
```

### Quoted node names and the node symbol @
In order to differentiate the parentheses of a function call from the parentheses defining Newick structure, quoted node names are used. The quotes surrounding each node will be removed and the contents inside will be processed as python code. If no quotes are present, as in the previous examples, all parenthesis are assumed to be part of the Newick structure. In order to ensure that the pattern is being processed correctly, set the quoted_node_names to False when not quoting node names. You can set quoted_node_names to True when they are used but this is assumed by default. In order to access a method on a node, use the @ symbol to represent the node.

```
# Example4: Find a tree where sample_1 and sample_2 are siblings.
pattern1 = TreePattern(' (sample_1, sample_2) ; ', quoted_node_names=False)

# Example 5: Find a tree where sample_2 and another leaf are siblings where a leaf is determined by number of children.
pattern2 = TreePattern(""" ('len(@.children)==0', 'sample_2') ; """, quoted_node_names=True)

# Example 6: Find a tree where sample_1 and another leaf are siblings by accessing the the is_leaf method.
pattern3 = TreePattern(""" ('sample_1', '@.is_leaf()') ; """, quoted_node_names=True)
```

### To Run
To run, use the find_match() function. By default, find_match will look for one match. If every match needs to be returned, set maxhits to None. To find the number of matches returned, use len().

```

# Example 6: Find the parent node of the siblings sample_1 and sample_2
tree = Tree("((sample_1,sample_2)ancestor_a,(sample_1,sample_2)ancestor_b)root;", format = 8)
pattern = TreePattern(' (sample_1, sample_2) ; ', quoted_node_names=False)
solution = list(pattern.find_match(tree, None))
print("The number of solutions are: ", len(solution))

```
The following tutorial shows the previous examples in more detail.


### Tutorial 1: Introduction to patterns using TreeMatcher.

```
    tree = Tree("((sample_1,sample_2)ancestor_a,(sample_1,sample_2)ancestor_b)root;", format=8)
    print tree

    border = "\n" + "#" * 110 + "\n"

    #######################################################
    print(border)
    print("Find all nodes named sample_1.")
    print(border)
    #######################################################

    # search for the name attribute.
    # The name is quoted but the node is not so quoted_node_names is set to False.
    pattern1_v1 = """ @.name=="sample_1" ; """
    pattern1_v1 = TreePattern(pattern1_v1, quoted_node_names=False)  # TP Instance
    solution = pattern1_v1.find_match(tree, None)
    print("version 1", list(solution))

    # When no attribute is given, the node name is assumed
    pattern1_v2 = """ sample_1 ; """
    pattern1_v2 = TreePattern(pattern1_v2, quoted_node_names=False)
    solution = pattern1_v2.find_match(tree, None)
    print("version 2", list(solution))

    # Find the total number of pattern2 matches
    solution = len(list(pattern1_v2.find_match(tree, None)))
    print("The number of solutions for pattern 1 is:", solution)

    #######################################################
    print(border)
    print("Find a tree where sample_1 and sample_2 are siblings.")
    print(border)
    #######################################################

    # Only need to find if there is a single match so maxhits=1
    pattern2_v1 = """ (sample_1, sample_2) ; """  # comma is used separate sibling nodes
    pattern2_v1 = TreePattern(pattern2_v1, quoted_node_names=False)  # create the TreePattern Instance
    solution = pattern2_v1.find_match(tree, maxhits=1)
    print("solution ", list(solution))

    #If you want to know if the match exists at a specific node, use match()
    solution1 = pattern2_v1.match(tree.children[0])
    solution2 = pattern2_v1.match(tree.children[1])
    print("solution 1 is", solution1)
    print("solution 2 is", solution2)

    # If you want all matches, use maxhits value of None.
    all_solutions = list(pattern2_v1.find_match(tree, None))
    print("All solutions for pattern 2 are:", all_solutions)
    t = PhyloTree(
        "((((((((((((((((Human_1, Chimp_1), (Human_2, (Chimp_2, Chimp_3))), ((Fish_1, (Human_3, Fish_3)), Yeast_2)), Yeast_1), Chimp_1), (Human_2, (Chimp_2, Chimp_3))), ((Fish_1, (Human_3, Fish_3)), Yeast_2)), Yeast_1), Chimp_1), (Human_2, (Chimp_2, Chimp_3))), ((Fish_1, (Human_3, Fish_3)), Yeast_2)), Yeast_1), Chimp_1), (Human_2, (Chimp_2, Chimp_3))), ((Fish_1, (Human_3, Fish_3)), Yeast_2)), Yeast_1);", format=8)
    t.set_species_naming_function(lambda n: n.name.split("_")[0] if "_" in n.name else '')
    t.get_descendant_evol_events()
    cache = TreePatternCache(t)
    pattern = TreePattern(
        """  (('n_duplications(@) > 0')'n_duplications(@) > 0 ')'contains_species(@, ["Chimp", "Human"])' ; """)

    #basic usage
    start_time = time.time()
    for i in range(0, 1000):
        list(pattern.find_match(t, maxhits=None))
    end_time = time.time()
    total_time= (end_time - start_time) / 1000.00
    print("time without cache", total_time)


    # Using Cache
    start_time_cache = time.time()
    for i in range(0, 1000):
        list(pattern.find_match(t, maxhits=None, cache=cache))
    end_time_cache = time.time()
    total_time_cache = (end_time_cache - start_time_cache) / 1000.00
    print("time with cache", total_time_cache)


    # Expanding vocabulary
    class MySyntax(PatternSyntax):
	    def my_nice_function(self, node):
		    return node.species == 'Chimp'

    my_syntax = MySyntax()

    pattern = """ 'my_nice_function(@)'; """
    t_pattern = TreePattern(pattern, syntax=my_syntax)
    for match in t_pattern.find_match(t, cache):
	print(list(match))

```

### The results of the Tutorial 1 are as follows:

```

      /-sample_1
   /-|
  |   \-sample_2
--|
  |   /-sample_1
   \-|
      \-sample_2

##############################################################################################################

Find all nodes named sample_1.

##############################################################################################################

('version 1', [Tree node 'sample_1' (0x10ac1365), Tree node 'sample_1' (0x10ac3315)])
('version 2', [Tree node 'sample_1' (0x10ac1365), Tree node 'sample_1' (0x10ac3315)])
('The number of solutions for pattern 1 is:', 2)

##############################################################################################################

Find a tree where sample_1 and sample_2 are siblings.

##############################################################################################################

('solution ', [Tree node 'ancestor_a' (0x108f09c9)])
('solution 1 is', True)
('solution 2 is', True)
('All solutions for pattern 2 are:', [Tree node 'ancestor_a' (0x108f09c9), Tree node 'ancestor_b' (0x1091024d)])
```

A short list of commonly used constraints is given in the following table.

Table 1: Examples of common constraints.

|  type                     |custom|  syntax example       						            | example meaning       				        |  Comments																        |
| --------------------------|:-:|:---------------------------------------------------------:|:---------------------------------------------:|:-----------------------------------------------------------------------------:|
| node                      |   | @	            						                    |a  node, default for nodes left blank	        | Use @.attribute to access attribute, function(@) to access function           |
| node name                 |   | node_name, "node_name", or @.name=="node_name"	        | when attribute not specified, name is assumed | Looking for multiple names, use list: @.name in ("sample1","sample2")         |
| distance                  |   | @.dist >= 0.5     					                    | branch length no less than 0.5		        | Use any of the following: <, <=, ==, >=, !=								    |
| support                   |   | @.support > 0.9	            		                    | Has a support value greater than 0.90	        | 																		        |
| species                   |   | @.species=="Homo sapiens"	    		                    | Homo sapiens is species of node		        | See set_species_naming_function()	for details							        |
| scientific name           |   | @.sci_name == Euarchontoglires 		                    | scientific name is Euarchontoglires	        | See annotate_ncbi_taxa() function for details 						        |
| rank                      |   | @.rank == subfamily 					                    | node is ranked at the subfamily level	        | See annotate_ncbi_taxa() function for details							        |
| taxonomic id              |   | @.taxid == 207598						                    | 20758 is the taxid of the node			    | See annotate_ncbi_taxa() function for details							        |
| number of children        |   | len(@.children)						                    | binary tree internal node has 2, leaf hss 0   | use quoted node names to differentiate parentheses from Newick Structure	    |
| size of subtree           |   | @.get_descendants() > 5							        | size of tree  is greater than 5               | number of descendants												            |
| number of leaves          |   | len(@) > 2                                                | number of leaves is greater than 2            | number of leaves descending from a node                                       |
| lineage                   | * | 9606 in @.lineage or "Homo sapiens" in @.named_lineage    | Homo sapiens in @.lineage				        | Find NCBI taxonomy ID or the full scientific name	in a node's lineage	        |
| species in descendant node| * | contains_species(@, ["Pan troglodytes", "Homo sapiens"])	| Find species in the last at or below node     | species at a node and any of it's descendants							        |
| leaf name                 | * | contains_leaves(@, ["Chimp_2", "Chimp_3"])		        | Pan_troglodytes_1 is descendant leaf name	    | Find the leaf name within a list of leaf names                                |
| number of duplications    | * |  		n_duplications(@) > 0                               | Number of duplications beyond and including this node is greater than zero.	    | number of duplication events at or below a node  |
| number of speciations     | * |  		n_speciations(@) > 0                                | Number of speciations beyond and including this node is greater than zero.	    | number of speciation events at or below a node  |

* functions do not exist outside of treematcher classes.



### Advanced Topics

#### optimization

Virtually any attribute available in ETE can be searched for on a tree, however, the larger the structure the more complex the pattern is, the more computationally intensive the search will be. Large Newick trees with complex conditional statements calling functions that require several tree traversals is not recommended.
Instead, break complex patterns into smaller searches. If conditional statements are used, try putting the part of the search that you think will be faster first.

#### Using a cache
For trees with thousands of nodes, you can speed up a search by using a cache. The same cache can be used with multiple patterns.

```
# Example 7:
cache = TreePatternCache(t)
solution = list(pattern.find_match(t, maxhits=None, cache=cache))
```

####  Custom Functions
You can use your own custom functions and syntax in treematcher.  In the following example, a custom function is created in a custom class called MySyntax.

```
# Example 8: Expanding vocabulary
class MySyntax(PatternSyntax):
	def my_nice_function(self, node):
		return node.species == 'Chimp'

my_syntax = MySyntax()

pattern = """ 'my_nice_function(@)'; """
t_pattern = TreePattern(pattern, syntax=my_syntax)
for match in t_pattern.find_match(t, cache):
	print(list(match))

```

### Command line tool
|  argument       						| meaning       						                                                  |
| --------------------------------------|:---------------------------------------------------------------------------------------:|
| -p								    | a list of patterns in newick format (filenames with one per file or quoted strings)     |
| -t								    | a list of trees in newick format (filenames or quoted strings)                          |
|-v                                     | prints the current pattern, prints which trees (by number) do not match the pattern     |
| --tree_format							| format for trees, default = 1	                            		                      |
| --quoted_node_names 					| default = True					                            	                      |
| --cache            					| name of cache, default = None					                  	                      |
| --maxhits          					| number of matches returned, default = 1   						                      |
| --src_tree_list                       | path to a file containing many target trees, one per line                               |
| --pattern_tree_list                   | path to a file containing many pattern trees, one per line                              |
| --render                              | filename (.SVG, .PDF, or .PNG), to render the tree image                                |
| --tab                                 | output results in tab delimited format, default if -o used and ascii not specified      |
| --ascii                               | output results in ascii format                                                          |

examples:
Read patterns from a file called MyPatterns.txt and apply to each tree in MyTargetTrees.txt, output the results of each pattern in separate files called treematches0.txt, treematches1.txt, etc
If there is only one pattern, the result file will not be numbered.
``` ete3 treematcher --pattern_tree_list "MyPattern.txt" --tree_format 8 --src_tree_list "MyTargetTrees.txt" -o treematches.txt ```

Provide the pattern and tree as strings and print the result to the terminal.
```ete3 treematcher -p "(e,d);" --tree_format 8 -t "(c,(d,e)b)a;" ```

The render option will save each match as an image. If there are multiple patterns, numbers will be used to designate each pattern starting from 0.
If there are multiple matches, and underscore is used with a number for each match starting with 0. If I had two

``` ete3 treematcher --pattern_tree_list "MyPatterns.txt" --tree_format 8 --src_tree_list "MyTargetTrees.txt" --render treematches.png ```


