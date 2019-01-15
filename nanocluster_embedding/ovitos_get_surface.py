from ovito.io import import_file
from ovito.modifiers import ConstructSurfaceModifier
from ovito.modifiers import DeleteSelectedParticlesModifier
from ovito.modifiers import SelectParticleTypeModifier
import sys

# Load a particle structure and construct its geometric surface:
fname = sys.argv[1]
node = import_file(fname, columns=["Particle Type", "Position.X", "Position.Y",
					"Position.Z"])
mod = ConstructSurfaceModifier(radius = 2.9)
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
