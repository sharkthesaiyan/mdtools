from ovito.io import import_file
from ovito.modifiers import ConstructSurfaceModifier
from ovito.modifiers import DeleteSelectedParticlesModifier
from ovito.modifiers import SelectParticleTypeModifier

# Load a particle structure and construct its geometric surface:
#fname = "si50mev_lastframe.xyz"
fname = "ti60mev_lastframe.xyz"
node = import_file(fname, columns=["Particle Type", "Position.X", "Position.Y",
					"Position.Z"])
mod = ConstructSurfaceModifier(radius = 2.9)
mod2 = SelectParticleTypeModifier()
mod2.types = {2, 3}
node.modifiers.append(mod2)

mod3 = DeleteSelectedParticlesModifier()
node.modifiers.append(mod3)

node.modifiers.append(mod)
node.compute()

# Query computed surface properties:
print("Surface area: %f" % node.output.attributes['ConstructSurfaceMesh.surface_area'])
print("Solid volume: %f" % node.output.attributes['ConstructSurfaceMesh.solid_volume'])
fraction = node.output.attributes['ConstructSurfaceMesh.solid_volume'] / node.output.cell.volume
print("Solid volume fraction: %f" % fraction)

# Export the surface triangle mesh to a VTK file.
mesh = node.output.surface
mesh.export_vtk('surface.vtk', node.output.cell)
