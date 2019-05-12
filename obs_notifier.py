import time
from typing import Optional

from obswebsocket import obsws, requests, base_classes


class GetSceneItemProperties(base_classes.Baserequests):
    """Gets the scene specific properties of the specified source item.

    :Arguments:
       *scene*
            type: String (optional)
            the name of the scene that the source item belongs to. Defaults to the current scene.
       *item_id*
            type: String
            The name of the source.
       *item_name*
            type: String
            The name of the source.
    :Returns:
       *scene*
            type: String
            The name of the scene.
       *item_name*
            type: String
            The name of the source.
       *item_id*
            type: String
            The id of the scene item.
       *item_position_x*
            type: int
            The x position of the source from the left.
       *item_position_y*
            type: int
            The y position of the source from the top.
       *item_position_alignment*
            type: int
            The point on the source that the item is manipulated from.
       *item_rotation*
            type: double
            The clockwise rotation of the item in degrees around the point of alignment.
       *item_scale_x*
            type: double
            The x-scale factor of the source.
       *item_scale_y*
            type: double
            The y-scale factor of the source.
       *item_crop_top*
            type: int
            The number of pixels cropped off the top of the source before scaling.
       *item_crop_right*
            type: int
            The number of pixels cropped off the right of the source before scaling.
       *item_crop_bottom*
            type: int
            The number of pixels cropped off the bottom of the source before scaling.
       *item_crop_left*
            type: int
            The number of pixels cropped off the left of the source before scaling.
       *item_visible*
            type: bool
            If the source is visible.
       *item_locked*
            type: bool
            If the source is locked.
       *item_bounds_type*
            type: String
            Type of bounding box.
       *item_bounds_alignment*
            type: int
            Alignment of the bounding box.
       *item_bounds_x*
            type: double
            Width of the bounding box.
       *item_bounds_y*
            type: double
            Height of the bounding box.
    """
    def __init__(self, item_name, scene=None):
        base_classes.Baserequests.__init__(self)
        self.name = "GetSceneItemProperties"
        self.datain["scene"] = None
        self.datain["item.name"] = None
        self.datain["item.id"] = None
        self.datain["item.position.x"] = None
        self.datain["item.position.y"] = None
        self.datain["item.position.alignment"] = None
        self.datain["item.rotation"] = None
        self.datain["item.scale.x"] = None
        self.datain["item.scale.y"] = None
        self.datain["item.crop.top"] = None
        self.datain["item.crop.right"] = None
        self.datain["item.crop.bottom"] = None
        self.datain["item.crop.left"] = None
        self.datain["item.visible"] = None
        self.datain["item.locked"] = None
        self.datain["item.bounds.type"] = None
        self.datain["item.bounds.alignment"] = None
        self.datain["item.bounds.x"] = None
        self.datain["item.bounds.y"] = None
        self.dataout["item"] = item_name
        self.dataout["scene-name"] = scene

    def getScene(self):
        return self.datain["scene"]

    def getItem_name(self):
        return self.datain["item.name"]

    def getItem_id(self):
        return self.datain["item.id"]

    def getItem_position_x(self):
        return self.datain["item.position.x"]

    def getItem_position_y(self):
        return self.datain["item.position.y"]

    def getItem_position_alignment(self):
        return self.datain["item.position.alignment"]

    def getItem_rotation(self):
        return self.datain["item.rotation"]

    def getItem_scale_x(self):
        return self.datain["item.scale.x"]

    def getItem_scale_y(self):
        return self.datain["item.scale.y"]

    def getItem_crop_top(self):
        return self.datain["item.crop.top"]

    def getItem_crop_right(self):
        return self.datain["item.crop.right"]

    def getItem_crop_bottom(self):
        return self.datain["item.crop.bottom"]

    def getItem_crop_left(self):
        return self.datain["item.crop.left"]

    def getItem_visible(self):
        return self.datain["item.visible"]

    def getItem_locked(self):
        return self.datain["item.locked"]

    def getItem_bounds_type(self):
        return self.datain["item.bounds.type"]

    def getItem_bounds_alignment(self):
        return self.datain["item.bounds.alignment"]

    def getItem_bounds_x(self):
        return self.datain["item.bounds.x"]

    def getItem_bounds_y(self):
        return self.datain["item.bounds.y"]


class SetSceneItemProperties(base_classes.Baserequests):
    """Sets the scene specific properties of a source. Unspecified properties will remain unchanged.

    :Arguments:
       *scene*
            type: String (optional)
            the name of the scene that the source item belongs to. Defaults to the current scene.
       *item_name*
            type: String
            The name of the item.
       *item_id*
            type: int
            The id of the item.
       *item_position_x*
            type: int
            The new x position of the item.
       *item_position_y*
            type: int
            The new y position of the item.
       *item_position_alignment*
            type: int
            The new alignment of the item.
       *item_rotation*
            type: double
            The new clockwise rotation of the item in degrees.
       *item_scale_x*
            type: double
            The new x scale of the item.
       *item_scale_y*
            type: double
            The new y scale of the item.
       *item_crop_top*
            type: int
            The new amount of pixels cropped off the top of the source before scaling.
       *item_crop_bottom*
            type: int
            The new amount of pixels cropped off the bottom of the source before scaling.
       *item_crop_left*
            type: int
            The new amount of pixels cropped off the left of the source before scaling.
       *item_crop_right*
            type: int
            The new amount of pixels cropped off the right of the source before scaling.
       *item_visible*
            type: bool
            The new visibility of the item. 'true' shows source, 'false' hides source.
       *item_locked*
            type: bool
            The new locked of the item. 'true' is locked, 'false' is unlocked.
       *item_bounds_type*
            type: String
            The new bounds type of the item.
       *item_bounds_alignment*
            type: int
            The new alignment of the bounding box. (0-2, 4-6, 8-10)
       *item_bounds_x*
            type: double
            The new width of the bounding box.
       *item_bounds_y*
            type: double
            The new height of the bounding box.
    """
    def __init__(self,
                 item_name,
                 item_position_x=None,
                 item_position_y=None,
                 item_position_alignment=None,
                 item_rotation=None,
                 item_scale_x=None,
                 item_scale_y=None,
                 item_crop_top=None,
                 item_crop_bottom=None,
                 item_crop_left=None,
                 item_crop_right=None,
                 item_visible=None,
                 item_locked=None,
                 item_bounds_type=None,
                 item_bounds_alignment=None,
                 item_bounds_x=None,
                 item_bounds_y=None,
                 scene=None):
        base_classes.Baserequests.__init__(self)
        self.name = "SetSceneItemProperties"
        self.dataout["item"] = item_name
        self.dataout["position.x"] = item_position_x
        self.dataout["position.y"] = item_position_y
        self.dataout["position.alignment"] = item_position_alignment
        self.dataout["rotation"] = item_rotation
        self.dataout["scale.x"] = item_scale_x
        self.dataout["scale.y"] = item_scale_y
        self.dataout["crop.top"] = item_crop_top
        self.dataout["crop.bottom"] = item_crop_bottom
        self.dataout["crop.left"] = item_crop_left
        self.dataout["crop.right"] = item_crop_right
        self.dataout["visible"] = item_visible
        self.dataout["locked"] = item_locked
        self.dataout["bounds.type"] = item_bounds_type
        self.dataout["bounds.alignment"] = item_bounds_alignment
        self.dataout["bounds.x"] = item_bounds_x
        self.dataout["bounds.y"] = item_bounds_y
        self.dataout["scene-name"] = scene


class ObsNotifier:
    def __init__(self,
                 host: str,
                 port: int,
                 password: str) -> None:
        self._ws = obsws(host, port, password)
        self._ws.connect()

    def notify(self, amount: int, memo: Optional[str]) -> None:
        self._ws.call(
            SetSceneItemProperties('donation_group', item_visible=True),
        )
        text = f'Someone just sent {amount} satoshis'
        if memo is not None:
            text += f' and said: \n{memo}'
        self._ws.call(
            requests.SetSourceSettings(
                'donation_text',
                {'text': text},
            )
        )
        time.sleep(10.0)
        self._ws.call(
            SetSceneItemProperties('donation_group', item_visible=False),
        )


if __name__ == '__main__':
    notifier = ObsNotifier('localhost', 4444, 'red riding hood')
    notifier.notify(1000, 'hey there cute boiii')
