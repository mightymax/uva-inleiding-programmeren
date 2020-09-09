def print_paths(path, destination, edges):
    if path[-1] == destination: # stop condition
        print("path: ", path)

    # finds the next possible node in path and adds it to the current path,
    # also removes the last node if a path reaches destination E
    else:    
        for edge in edges:
            nextStep = ''
            # Tuples in edges may have either the first or second element equal 
            # to the current last step of the path, so we need to check that:
            if edge[0] == path[-1]:
                nextStep = edge[1]
            elif edge[1] == path[-1]:
                nextStep = edge[0]
                
            # if the next step is not already in our path, append it to the path 
            # and run this function again with the updated path
            if nextStep and nextStep not in path:
                print_paths(path + [nextStep], destination , edges)
                
            
print_paths(['A'],'E',[ ('A','B'), ('A','D'), ('B','C'), ('B','D'), ('C','E'), ('C','F'), ('C','D'), ('D','F'), ('E','F') ])