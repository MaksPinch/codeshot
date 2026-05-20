from django.urls import reverse
from rest_framework.test import APIClient


def test_homepage():
    client = APIClient()
    url = reverse("home")
    response = client.get(url)

    assert response.status_code == 200
    assert b"CodeShot" in response.content
    assert b'name="code"' in response.content
    assert b'name="language"' in response.content
    assert b'name="filename"' in response.content
    assert b"Generate preview" in response.content


# что выдает response.content
# >>> print(response.content)
# b'<!doctype html>\n<html lang="en">\n
# <head>\n
#    <meta charset="UTF-8" />\n
#     <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n
#    <title>CodeShot</title>\n
#   </head>\n
#   <body>\n
#     <main>\n
#       <section>\n
#        <h1>CodeShot</h1>\n
#         <p>Create syntax-highlighted code previews.</p>\n
#       </section>\n
#     <section>\n
#      <form method="post">\n
#          <input type="hidden" name="csrfmiddlewaretoken" value="7uCBBoPpayc3rzQsY68ILszw7lTlcyvCLvPvlxMYufziONFtr8Gd5D38cZ4wsJuJ"> <label for="id_language">Language</label>\n
#           <select id="id_language" name="language">\n
#            <option value="python">Python</option>\n
#          <option value="javascript">JavaScript</option>\n
#         </select>\n
#          <label for="id_filename">Filename</label>\n
#           <input id="id_filename" type="text" name="filename" value="main.py" />\n
#         <label for="id_code">Code</label>\n
#          <textarea id="id_code" name="code" rows="12">\nprint("Hello, CodeShot!")\n</textarea\n
#          >\n
#       <button type="submit">Generate preview</button>\n
#        </form>\n
#    </section>\n
#   <section aria-label="Preview">\n
#       <h2>Preview</h2>\n
#      <pre><code>Preview will appear here.</code></pre>\n
#      </section>\n
#     </main>\n
#  </body>\n
# </html>\n'
# >>>
