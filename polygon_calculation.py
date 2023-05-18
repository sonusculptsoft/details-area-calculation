import geopandas as gpd
import largestinteriorrectangle as lir
import numpy as np
from shapely.geometry import MultiPolygon, Polygon, LineString


def return_rectangle(polygon):
    rectangle = lir.lir(polygon)

    x, y, width, height = rectangle

    top_left = (x, y)
    top_right = (x + width, y)
    bottom_right = (x + width, y + height)
    bottom_left = (x, y + height)

    return [top_left, bottom_left, bottom_right, top_right]


def remove_recangle_from_polygon(polygon, rectangle):
    # Create GeoDataFrame objects from the polygons
    gdf_polygon = gpd.GeoDataFrame(geometry=[polygon])
    gdf_rectangle = gpd.GeoDataFrame(geometry=[rectangle])

    # Compute the difference between the polygon and rectangle
    gdf_difference = gpd.overlay(gdf_polygon, gdf_rectangle, how="difference")

    # Convert the resulting GeoDataFrame back to a Shapely Polygon
    # return new_polygon

    return gdf_difference.geometry.unary_union


def plot_rectangle(new_polygon):
    new_child_polygon_list = []
    # Plot the new polygon(s)
    if isinstance(new_polygon, Polygon):
        pts = np.array([new_polygon.exterior.coords], np.int32)
        new_rectangle = return_rectangle(polygon=pts)
        child_rectangel = Polygon(new_rectangle)
        return_response.append(
            {
                "is_rectangle": True,
                "coords": list(child_rectangel.exterior.coords),
            }
        )

        new_child_polygon = remove_recangle_from_polygon(
            polygon=new_polygon, rectangle=child_rectangel
        )
        new_child_polygon_list.append(new_child_polygon)
    elif isinstance(new_polygon, MultiPolygon):
        new_polygon_series = gpd.GeoSeries(new_polygon)
        for child_polygon in new_polygon_series.explode(index_parts=True):
            if child_polygon.area >= 1000:
                pts = np.array([child_polygon.exterior.coords], np.int32)

                new_rectangle = return_rectangle(polygon=pts)
                child_rectangel = Polygon(new_rectangle)
                return_response.append(
                    {
                        "is_rectangle": True,
                        "coords": list(child_rectangel.exterior.coords),
                    }
                )

                new_child_polygon = remove_recangle_from_polygon(
                    polygon=child_polygon, rectangle=child_rectangel
                )
                new_child_polygon_list.append(new_child_polygon)
            else:
                return_response.append(
                    {
                        "is_rectangle": False,
                        "coords": list(child_polygon.exterior.coords),
                    }
                )
    return new_child_polygon_list


def plot_polygon(new_polygon, is_rectangle=False):
    # Plot the new polygon(s)
    if isinstance(new_polygon, Polygon):
        return_response.append(
            {"is_rectangle": is_rectangle, "coords": list(new_polygon.exterior.coords)}
        )

    if isinstance(new_polygon, MultiPolygon):
        new_polygon_series = gpd.GeoSeries(new_polygon)
        for child_polygon in new_polygon_series.explode(index_parts=True):
            return_response.append(
                {
                    "is_rectangle": is_rectangle,
                    "coords": list(child_polygon.exterior.coords),
                }
            )


return_response = []


def manage(region_list):
    for region in region_list:
        polygon = np.array([region], np.int32)

        sheplay_polygon = Polygon(region)

        # Check if it is a rectangle
        if sheplay_polygon.is_valid and sheplay_polygon.geom_type == "Polygon":
            # Check if opposite sides are parallel and equal in length
            sides = LineString(sheplay_polygon.exterior.coords)
            coords = sides.coords[:]
            opposite_sides = [
                LineString([coords[i], coords[j]]) for i, j in [(0, 2), (1, 3)]
            ]
            side_lengths = [opposite_sides[i].length for i in range(2)]
            is_rectangle = all(
                [abs(side_lengths[i] - side_lengths[i - 1]) < 1e-6 for i in range(2)]
            )

            if is_rectangle:
                print("sheplay_polygon is a rectangle")
                plot_polygon(sheplay_polygon, is_rectangle=True)
            else:
                print("sheplay_polygon is not a rectangle")

                new_rectangle = return_rectangle(polygon=polygon)

                # Define the polygon and rectangle
                sheplay_rectangle = Polygon(new_rectangle)
                return_response.append(
                    {
                        "is_rectangle": is_rectangle,
                        "coords": list(sheplay_rectangle.exterior.coords),
                    }
                )

                new_polygon = remove_recangle_from_polygon(
                    polygon=sheplay_polygon, rectangle=sheplay_rectangle
                )

                new_child_polygon = plot_rectangle(new_polygon=new_polygon)

                if len(new_child_polygon):
                    for new_cc_polygon in new_child_polygon:
                        cc = plot_rectangle(new_polygon=new_cc_polygon)
                        if len(cc):
                            for i in cc:
                                plot_polygon(i)
    return return_response


print(return_response)
