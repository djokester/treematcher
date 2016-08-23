import sys
from logging import log
from argparse import ArgumentParser
from .common import src_tree_iterator
from ..phylo import PhyloTree
from treematcher import TreePattern, TreePatternCache

DESC=''

#ete3 treematcher --pattern "(hello, kk);" --pattern-format 8 --tree-format 8 --trees "(hello,(1,2,3)kk);" --quoted-node-names


def populate_args(treematcher_args_p):

    treematcher_args = treematcher_args_p.add_argument_group('TREEMATCHER OPTIONS')


    treematcher_args.add_argument("--quoted_node_names", dest="quoted_node_names",
                              action="store_true",
                              help="True if using quotes to designate node names in the pattern. Otherwise False.")
    treematcher_args.add_argument("--tree_format", dest="tree_format",
                              type=int,
                              default=0,
                              help="A number 0-8 designating Newick format.")
    treematcher_args.add_argument("--maxhits", dest="maxhits",
                              nargs=1,
                              type=int,
                              default=0,
                              help="The number of matches to return. Default is 0 which returns all matches.")
    treematcher_args.add_argument("--cache", dest="cache",
                              action="store_true",
                              help="True if a cache is to be used. Otherwise False.")
    treematcher_args.add_argument("--tab", dest="taboutput",
                              action="store_true",
                              help="output results in tab delimited format")
    treematcher_args.add_argument("--ascii", dest="asciioutput",
                              action="store_true",
                              help="output results in ascii format")
    treematcher_args.add_argument("-p", dest='pattern_trees',
                              type=str, nargs="*",
                              help=("a list of trees in newick format (filenames or"
                              "quoted strings)"))
    treematcher_args.add_argument("--pattern_tree_list", dest="pattern_tree_list",
                              type=str,
                              help=("path to a file containing many pattern trees, one per line"))
    treematcher_args.add_argument("--render", dest="render",
                               type=str,
                               help="filename (.SVG, .PDF, or .PNG), to render the tree")

def run(args):
    if args.src_trees is None and args.src_tree_list is None:
        log.error('Please specify a tree to search (i.e. -t) ')
        sys.exit(-1)
    if not args.pattern_trees and not args.pattern_tree_list:
        log.error('Please specify a pattern to search for. (i.e. -p)')
        sys.exit(-1)

    if args.maxhits == 0:
        args.maxhits = None

    for pattern_num, p in enumerate(pattern_tree_iterator(args)):
        print("p is {}".format(p))
        pattern = TreePattern(p, quoted_node_names=args.quoted_node_names)

        if args.output:
            filename = args.output
            if len(list(pattern_tree_iterator(args))) > 1:
                if '.' in args.output:
                    filename = filename.replace('.', str(pattern_num) + '.')
                else:
                    filename += str(pattern_num)

            outputfile = open(filename, 'w')

        if args.verbosity > 2:
            print("Pattern is: ")
            print(pattern)

        for nw in src_tree_iterator(args):
            print("nw is {}".format(nw))
            t = PhyloTree(nw, format=args.tree_format)

            if args.cache:
                cache = TreePatternCache(t)
            else:
                cache = None

            matches = list(pattern.find_match(t, maxhits=args.maxhits, cache=cache))
            print("matches are {}".format(matches))

            if args.render:
                from . import ete_view
                ts = ete_view.TreeStyle()
                ts.layout_fn = ete_view.maptrees_layout
                ts.show_scale = False
                ts.tree_width = 400
                [match.render(args.image, tree_style=ts) for match in matches]

            if args.output:
                if args.asciioutput:
                    for match in matches:
                        outputfile.write(str(match) + '\n')
                else:  #args.taboutput
                    outputfile.write('\t'.join([match.write(features=[]) for match in matches]))

            else:
                for match in matches:
                    print(match)


    if args.output:
        outputfile.close()


def pattern_tree_iterator(args):
    if not args.pattern_trees and not sys.stdin.isatty():
        log.debug("Reading patterns from standard input...")
        args.pattern_trees = sys.stdin
    if args.pattern_trees:
        for p_tree in args.pattern_trees:
            yield p_tree.strip()
    elif args.pattern_tree_list:
        for line in open(args.pattern_tree_list):
            line = line.strip()
            if line:
                yield line


if __name__ == "__main__":
    parser = ArgumentParser()
    populate_args(parser)
    args = parser.parse_args(sys.argv[1:])
    run(args)



    '''
    #add in ete.py

     from . import (ete_split, ete_expand, ete_annotate, ete_ncbiquery, ete_view,
               ete_generate, ete_mod, ete_extract, ete_compare, ete_evol,
               ete_maptrees, ete_treematcher)


    # -treematcher-
    treematcher_args_p = subparser.add_parser("treematcher", parents=[source_args_p, main_args_p],
                                           description=ete_treematcher.DESC)
    treematcher_args_p.set_defaults(func=ete_treematcher.run)
    ete_treematcher.populate_args(treematcher_args_p)


    '''