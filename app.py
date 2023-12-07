from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from PIL import Image
import io
import base64
import torch
from torchvision import models

alexnet = models.AlexNet()

resnet = models.resnet101(pretrained=True)

from torchvision import transforms

preprocess = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


# Create flask instance
app = Flask(__name__)

app.config["SECRET_KEY"] = "123"


class UploadForm(FlaskForm):
    image = FileField("Upload Image", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a URL route in our application for "/"
@app.route("/", methods=["GET", "POST"])
def index():
    form = UploadForm()

    if form.validate_on_submit():
        # Get the uploaded image
        uploaded_image = form.image.data

        # Process the image using PIL
        image = Image.open(uploaded_image)
        # Add your image processing logic here
        img_t = preprocess(image)
        batch_t = torch.unsqueeze(img_t, 0)
        resnet.eval()
        out = resnet(batch_t)
        with open("data/imagenet_classes.txt") as f:
            labels = [line.strip() for line in f.readlines()]

        _, index = torch.max(out, 1)

        percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
        percentage = percentage[index[0]].item()
        result = labels[index[0]]

        # Save the processed image to a BytesIO object
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Encode the image data to Base64
        img_data_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

        # Render a new template with the processed image
        return render_template(
            "results.html",
            img_data_base64=img_data_base64,
            result=result,
            percentage=percentage,
        )

    return render_template("index.html", form=form)
