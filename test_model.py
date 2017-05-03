from pyFS import model

m = model.Model('C:\Dev\pyFS\Model', 'test model')
for node in range(1, 12):
    m.create_node(node, node - 1, 0, 0, 0)
for element in range(1, 11):
    m.create_beam_element(N1=element, N2=element + 1)

print(m.nodes)
print(m.beam_elements)
m.write_MDL_file()
#m.initialise_model()