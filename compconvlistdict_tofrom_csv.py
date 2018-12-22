import pandas as pd

def save_comp_convlist_to_csv(comp_convlist_dict, savepath = "comp_convlist_df.csv"):
    
    # [[1, 2], [3, 4, 5]] to "1,2 3,4,5"
    def list_list_to_str(ll):
        return " ".join(
            [",".join(list(map(str, l)))
                for l in ll]
            )
        
    convlists_map = comp_convlist_dict.values()
    
    convlist_strs = list(map(list_list_to_str, convlists_map))
    
    # make df
    comp_convlist_df = pd.DataFrame({
        "company": list(comp_convlist_dict.keys()),
        "convlist_str": convlist_strs
        })
    
    comp_convlist_df.to_csv(savepath, index = False)

def load_comp_convlist_from_csv(path = "comp_convlist_df.csv"):
    
    # "1,2 3,4,5" to [[1, 2], [3, 4, 5]]
    def str_to_convlist(s):
        conv_strs = s.split(" ")
        convlist = [
            list(map(int, s.split(",")))
            for s in conv_strs
            ]
        return convlist
    
    # read csv
    df = pd.read_csv(path)
    comps = df["company"].values
    convlist_strs = df["convlist_str"]
    convlists_map = map(str_to_convlist, convlist_strs)
    
    # turn to dict
    comp_convlist_dict = dict(zip(
        comps, convlists_map
        ))
    return comp_convlist_dict