def details(order):
    no_ipix_cells = 12*4**(order)
    print(f"Order {order} has {no_ipix_cells} number of ipix cells")
    
def current_order(order):
    nside = 2**order
    hp = HEALPix(nside=nside, order = 'nested', frame = ICRS())
    coord = SkyCoord(table["_RA"], table["_DE"], frame= 'icrs', unit = 'deg')
    ipix = hp.skycoord_to_healpix(coord)
    main_list = np.sort(np.unique(np.abs((ipix))))
    string_list = " ".join(map(str, main_list))
    
    return main_list
    
def increase_order(order, main_list):
    
    nside = 2**order
    hp = HEALPix(nside=nside, order = 'nested', frame = ICRS())
    coord = SkyCoord(table["_RA"], table["_DE"], frame= 'icrs', unit = 'deg')
    ipix = hp.skycoord_to_healpix(coord)
    main_list = np.sort(np.unique(np.abs((ipix))))
    string_list = " ".join(map(str, main_list))
    
    combined_child_ipix = []
    for ipix in main_list:
        child_ipix = [(ipix << 2), (ipix << 2) + 1, (ipix << 2) + 2, (ipix << 2) + 3]
        combined_child_ipix.extend(child_ipix)
    string_inc = " ".join(map(str, combined_child_ipix))
    
    return string_inc #This represents the list of ipix cells of the higher order in string format.
    
def My_MOC(order, main_list):
    
    main_list = current_order(order)
    
    MOC_Tree_child = []
    MOC_Tree_parent = []
    MOC_Tree_root = []

    if order == 0:
        MOC_Tree_root.extend(main_list)
        print(f'{order}/', MOC_Tree_root)
    else:
        j = 0
        while j < 12*(4)**(order):              

            ideal_siblings = [(j), (j+1), (j+2), (j+3)]

            if all(item in main_list for item in ideal_siblings):
                # All siblings are present
                # Replace with parent in the ideal siblings list, which is the first item in every 4 items

                MOC_Tree_parent.append(j>>2)

            else:
                if j in main_list:
                    MOC_Tree_child.append(j)

                if j+1 in main_list:
                    MOC_Tree_child.append(j+1)

                if j+2 in main_list:
                    MOC_Tree_child.append(j+2)

                if j+3 in main_list:
                    MOC_Tree_child.append(j+3)

            j = j + 4

        unique_MOC_Tree_c = np.unique(MOC_Tree_child)
        unique_MOC_Tree_p = np.unique(MOC_Tree_parent)

        #convert list into string

        parents_string = " ".join(map(str, unique_MOC_Tree_p))
        children_string = " ".join(map(str, unique_MOC_Tree_c))
        final_string = f"{order-1}/{parents_string}\n{order}/{children_string}"

        return final_string    