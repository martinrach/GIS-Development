import open3d as o3d

def visualize_data(data):
    geom = o3d.geometry.PointCloud()
    geom.points = o3d.utility.Vector3dVector(data)
    o3d.visualization.draw_geometries([geom])
