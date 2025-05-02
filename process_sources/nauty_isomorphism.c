#include "nauty_isomorphism.h"

double check_isomorphism_nauty(graph *graph1, graph *graph2, const int n, bool should_be_isomorphic) {
    DYNALLSTAT(int,lab1,lab1_sz);
    DYNALLSTAT(int,lab2,lab2_sz);
    DYNALLSTAT(int,ptn,ptn_sz);
    DYNALLSTAT(int,orbits,orbits_sz);
    DYNALLSTAT(int,map,map_sz);
    DYNALLSTAT(graph,g1,g1_sz);
    DYNALLSTAT(graph,g2,g2_sz);
    DYNALLSTAT(graph,cg1,cg1_sz);
    DYNALLSTAT(graph,cg2,cg2_sz);
    static DEFAULTOPTIONS_GRAPH(options);
    statsblk stats;
    options.getcanon = TRUE;

    const int m = SETWORDSNEEDED(n);
    nauty_check(WORDSIZE,m,n,NAUTYVERSIONID);
    DYNALLOC1(int,lab1,lab1_sz,n,"malloc");
    DYNALLOC1(int,lab2,lab2_sz,n,"malloc");
    DYNALLOC1(int,ptn,ptn_sz,n,"malloc");
    DYNALLOC1(int,orbits,orbits_sz,n,"malloc");
    DYNALLOC1(int,map,map_sz,n,"malloc");
    DYNALLOC2(graph,g1,g1_sz,n,m,"malloc");
    DYNALLOC2(graph,g2,g2_sz,n,m,"malloc");
    DYNALLOC2(graph,cg1,cg1_sz,n,m,"malloc");
    DYNALLOC2(graph,cg2,cg2_sz,n,m,"malloc");

    // Create canonical graphs
    const clock_t start = clock();
    densenauty(graph1,lab1,ptn,orbits,&options,&stats,m,n,cg1);
    densenauty(graph2,lab2,ptn,orbits,&options,&stats,m,n,cg2);

    // Compare canonically labelled graphs
    size_t k;
    for (k = 0; k < m*(size_t)n; ++k)
        if (cg1[k] != cg2[k]) break;
    bool is_isomorphic = k == m*(size_t)n;
    if (should_be_isomorphic != is_isomorphic) {
        printf("Error: graphs with n=%d vertexes should be is_isomorphic=%hhd but was is_isomorphic=%hhd\n", n, should_be_isomorphic, is_isomorphic);
        exit(EXIT_FAILURE);
    }
    const clock_t end = clock();

    return (double)(end - start) / CLOCKS_PER_SEC;
}
