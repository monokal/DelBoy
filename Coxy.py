from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Coxy is running.'


# Listing engine endpoints.
@app.route('/api/v1/listing/approve')
def approve_listing():
    pass


@app.route('/api/v1/listing/remove')
def remove_listing():
    pass


# Sale engine endpoints.
@app.route('/api/v1/sale/confirm')
def confirm_sale():
    pass


if __name__ == '__main__':
    app.run()
