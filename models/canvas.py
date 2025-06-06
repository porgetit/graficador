import json
from models.shapes import ShapeFactory

class Canvas:
    def __init__(self):
        self.shapes = []
        self.background_color = (255, 255, 255)

    def addShape(self, shape):
        self.shapes.append(shape)

    def removeShape(self, shape):
        self.shapes.remove(shape)

    def clear(self):
        self.shapes.clear()

    def to_json(self):
        shapes_data = []
        for shape in self.shapes:
            shape_type = None
            from models.shapes import Line, Circle, Rectangle, Polygon, Curve, EraseArea
            if isinstance(shape, Line):
                shape_type = "LINE"
            elif isinstance(shape, Circle):
                shape_type = "CIRCLE"
            elif isinstance(shape, Rectangle):
                shape_type = "RECTANGLE"
            elif isinstance(shape, Polygon):
                shape_type = "POLYGON"
            elif isinstance(shape, Curve):
                shape_type = "CURVE"
            elif isinstance(shape, EraseArea):
                shape_type = "ERASE_AREA"
            shape_data = {
                "type": shape_type,
                "points": shape.points,
                "color": shape.color,
                "lineWidth": shape.lineWidth,
                "algorithmType": shape.drawingAlgorithm.algorithmType
            }
            shapes_data.append(shape_data)
        canvas_data = {
            "background_color": self.background_color,
            "shapes": shapes_data
        }
        return json.dumps(canvas_data)

    def load_json(self, json_str):
        canvas_data = json.loads(json_str)
        self.background_color = tuple(canvas_data.get("background_color", (255, 255, 255)))
        shapes_data = canvas_data.get("shapes", [])
        self.shapes.clear()
        for data in shapes_data:
            shape_type = data.get("type")
            points = data.get("points")
            color = tuple(data.get("color"))
            lineWidth = data.get("lineWidth")
            algorithmType = data.get("algorithmType")
            shape = ShapeFactory.createShape(shape_type, points, color, lineWidth, algorithmType)
            self.shapes.append(shape)

    def removeShapesInArea(self, area_rect):
        """
        Elimina las figuras que intersectan con un área rectangular.

        Args:
            area_rect (pygame.Rect): Área rectangular de borrado.
        """
        shapes_to_remove = []
        for shape in self.shapes:
            if self.shapeIntersectsArea(shape, area_rect):
                shapes_to_remove.append(shape)
        for shape in shapes_to_remove:
            self.removeShape(shape)

    def shapeIntersectsArea(self, shape, area_rect):
        """
        Verifica si una figura intersecta con un área rectangular.

        Args:
            shape (Shape): Figura a verificar.
            area_rect (pygame.Rect): Área rectangular.

        Returns:
            bool: True si la figura intersecta con el área, False en caso contrario.
        """
        for point in shape.points:
            if area_rect.collidepoint(point):
                return True
        return False
