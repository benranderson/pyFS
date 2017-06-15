from pyFS import pyFS as pyFS

m = pyFS.pyFS('C:\Dev\pyFS\Model', 'test model',
              initialise_model=True).model_definition
for node in range(1, 12):
    m.create_node(node, node - 1, 0, 0, 0)
for element in range(1, 11):
    m.create_beam_element(element, N1=element, N2=element + 1)
for couple in range(1, 11):
    m.create_couple(couple, N1=couple, N2=couple+1)
for rest in range(1, 12):
    m.create_restraint(rest, Tx=True)

print(m.nodes)
print(m.beam_elements)
print(m.couples)
print(m.restraints)
print(m.geometries)
m.write_MDL_file()
# m.initialise_model()
