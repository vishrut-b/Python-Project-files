import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.coordinates import SkyCoord, ICRS, Angle
from astropy import units as u
from astropy_healpix import HEALPix

def details(order):
    no_ipix_cells = 12*4**(order)
    print(f"Order {order} has {no_ipix_cells} number of ipix cells")
    
def current_order(order):
    source = "II/7A/catalog"
    url = f"https://vizier.cds.unistra.fr/viz-bin/votable?-source={source}&-out.max=10000"
    table = Table.read(url, table_id="II/7A/catalog")
    nside = 2**order
    hp = HEALPix(nside=nside, order = 'nested', frame = ICRS())
    coord = SkyCoord(table["_RA"], table["_DE"], frame= 'icrs', unit = 'deg')
    ipix = hp.skycoord_to_healpix(coord)
    main_list = np.sort(np.unique(np.abs((ipix))))
    string_list = " ".join(map(str, main_list))
    
    return main_list
    
def increase_order(order, main_list):
    
    source = "II/7A/catalog"
    url = f"https://vizier.cds.unistra.fr/viz-bin/votable?-source={source}&-out.max=10000"
    table = Table.read(url, table_id="II/7A/catalog")
    
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
    
    source = "II/7A/catalog"
    url = f"https://vizier.cds.unistra.fr/viz-bin/votable?-source={source}&-out.max=10000"
    table = Table.read(url, table_id="II/7A/catalog")      
    lists_c = [[] for _ in range(order + 1)]
    MOC_Tree_root = []
    
    if order == 0:
        MOC_Tree_root.extend(mod.current_order(0))
        print(f'{order}/', MOC_Tree_root)
        return MOC_Tree_root
    else:
        while order != 0:
            j = 0
            lists_p = []
            
            while j < 12*(4)**(order):          

                ideal_siblings = [(j), (j+1), (j+2), (j+3)]

                if all(item in main_list for item in ideal_siblings):
                    lists_p.append(j>>2) # Creating the parent cell list
                    #print("lists_p =", lists_p)
                else:
                    if j in main_list:
                        lists_c[order].append(j)
                    if j+1 in main_list:
                        lists_c[order].append(j+1)
                    if j+2 in main_list:
                        lists_c[order].append(j+2)
                    if j+3 in main_list:
                        lists_c[order].append(j+3)

                j = j + 4
                
            main_list = lists_p
            order = order-1 
        
        
        result_string = '\n'.join([f'{i}/ {" ".join(map(str, sublist))}' for i, sublist in enumerate(lists_c, start=0)])
        return result_string