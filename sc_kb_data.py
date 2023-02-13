import pandas as pd

def update_notes(text):
    with open("notes.txt", "w") as file:
        file.write(text)

def get_notes():
    file = open("notes.txt", "r")
    return file.read()

def find_hierarchy_level(segments):
    # Create a dictionary to store the hierarchy level of each node
    hierarchy_level = {}
    # Iterate through each segment
    for segment in segments:
        # Set the hierarchy level of each node to 0 if it has not been visited before
        for node in segment:
            if node not in hierarchy_level:
                hierarchy_level[node] = 0
        # Assign hierarchy level to each segment node.
        if segment[0] != segment[1]:
            hierarchy_level[segment[1]] = hierarchy_level[segment[0]] + 1

    return hierarchy_level

def get_sc_data():
    
    ## get base data
    data = pd.read_csv('product.csv')
    
    segments = data[['product','part']].values.tolist()
    hierarchy_levels = find_hierarchy_level(segments)
    
    node_names = set(list(data['product'].unique()) + list(data['part'].unique()))
    nodes = pd.DataFrame([x for x in enumerate(node_names)],columns=['node','name'])
    
    links = pd.merge(data,nodes,how='inner',left_on='product',right_on='name').copy()
    links.rename(columns={'node':'from_node'},inplace=True)
    links = pd.merge(links,nodes,how='inner',left_on='part',right_on='name')
    links.rename(columns={'node':'to_node'},inplace=True)
    links.drop(columns=['name_x','name_y'],inplace=True)
    
    segments = data[['product','part']].values.tolist()
    
    return nodes,links

def get_risk_data():
    
    ## get base data
    data = pd.read_csv('product.csv')
    
    labels = set(list(data['product'].unique()) + list(data['part'].unique()))
    labels_lookup = pd.DataFrame([x for x in enumerate(labels)],columns=['code','component'])
    dataset = pd.merge(data,labels_lookup,how='inner',left_on='product',right_on='component').copy()
    dataset.rename(columns={'code':'product_code'},inplace=True)
    dataset = pd.merge(dataset,labels_lookup,how='inner',left_on='part',right_on='component')
    dataset.rename(columns={'code':'part_code'},inplace=True)
    dataset.drop(columns=['component_x','component_y'],inplace=True)
    
    return dataset, labels


def apply_rf(data):
    dataset = data.copy()
    dataset['total rating'] = dataset[['e-climate_impact', 'e-biodiversity', 's-human_trafficking','s-labor_rights', 'g-org_commitment', 'g-resiliency']].median(axis=1)
    dataset['total rating bin'] = pd.cut(dataset['total rating'],[0,25,50,75,100], labels=['0-25%','26-50%','51-75%','76-100%'])
    dataset.reset_index(inplace=True)
    node_color_scheme = pd.DataFrame(data=[["0-25%",'rgb(192, 192, 192)'],["26-50%",'rgb(192, 192, 192)'],["51-75%",'rgb(255, 100, 100)'],["76-100%",'rgb(255, 0, 0)']],columns=['rating','color'])
    dataset = pd.merge(dataset,node_color_scheme,left_on=['total rating bin'],right_on=['rating'], how='inner')
    dataset.sort_values(by=['total rating'],ascending=False, inplace=True)

    return dataset

def rollup_to_prod(data):
    dataset = pd.merge(data[['product','e-climate_impact', 'e-biodiversity', 's-human_trafficking','s-labor_rights', 'g-org_commitment', 'g-resiliency']].groupby(by=['product']).median(),data[['product','qty']].groupby(by=['product']).sum(), how='inner', on=['product']).copy()
    #dataset.reset_index(inplace=True)
    
    return dataset

def rollup_to_sup(data):
    dataset = pd.merge(data[['supplier','e-climate_impact', 'e-biodiversity', 's-human_trafficking','s-labor_rights', 'g-org_commitment', 'g-resiliency']].groupby(by=['supplier']).median(),data[['supplier','qty']].groupby(by=['supplier']).sum(), how='inner', on=['supplier']).copy()
    dataset.reset_index(inplace=True)
    
    return dataset

def rollup_to_country(data):
    dataset = pd.merge(data[['country','e-climate_impact', 'e-biodiversity', 's-human_trafficking','s-labor_rights', 'g-org_commitment', 'g-resiliency']].groupby(by=['country']).median(),data[['country','qty']].groupby(by=['country']).sum(), how='inner', on=['country']).copy()
    dataset.reset_index(inplace=True)
    
    return dataset
    
##    dataset = dataset.T
##    dataset['change'] = dataset[2022]-dataset[2021]
    

def get_vc_data(data):
    
    labels = set(list(data['product'].unique()) + list(data['part'].unique()))
    
    return data

def get_risk_sum3(data):
    
    dataset = []
    
    return dataset

def get_prod_risk_cat(data):
    
    dataset = data[['tier','product','e-climate_impact', 'e-biodiversity', 's-human_trafficking',
       's-labor_rights', 'g-org_commitment', 'g-resiliency','total rating']].groupby(by=['tier','product']).mean().copy()
    
    return dataset