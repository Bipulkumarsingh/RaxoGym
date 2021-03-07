from flask_restful import Resource, reqparse
from library.flask_uploads.flask_uploads import UploadNotAllowed
from flask import send_file
from werkzeug.datastructures import FileStorage
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from library.image import images
from src.response import Response
from models.admin import Admin
from src.constants import Constants

response = Response()
constants = Constants()


class UploadImage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('image',
                        type=FileStorage,
                        location='files')

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        user_id = get_jwt_identity()
        # folder = "profile_pic"
        try:
            claims = get_jwt_claims()
            user_public_id = claims['user']['public_id']
            data['image'].filename = user_public_id + '.' + data['image'].filename.split('.')[-1]
            # save image save(self, storage, folder=None, name=None)
            image_path = images.save_image(data['image'])
            # Here we only return the basename of the image and hide the internal folder structure from our user
            basename = images.get_basename(image_path)
            base_url = 'http://127.0.0.1:7000/image/' + basename
            # query = Admin.update_profile_pic(user_id, base_url)
            # constants.update_query(query)
            return response.profile_pic_update(base_url)
        except UploadNotAllowed:
            extension = images.get_extension(data['image'])
            return response.exception(extension)


class GetImage(Resource):
    def get(self, filename: str):
        """Return the requested images if it exists. Looks up inside the logged in user's folder."""
        user_id = get_jwt_identity()
        # folder = "profile_pic"
        if not images.is_filename_safe(filename):
            return {"message": f"{filename} filename is not valid"}, 200
        try:
            return send_file(images.get_path(filename))
        except FileNotFoundError:
            return {"message": "File not found"}, 200

    @jwt_required
    def delete(self):
        pass
