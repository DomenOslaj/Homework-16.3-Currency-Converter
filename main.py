#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template( "hello.html" )

class ConvertHandler(BaseHandler):
    def post(self):
        currency_from = self.request.get( "currency1" )
        currency_to = self.request.get( "currency2" )
        convert_number = float( self.request.get( "number" ))

        if currency_from == "EUR" and currency_to == "USD":
            result = float( convert_number * 1.119716 )

        elif currency_from == "EUR" and currency_to == "GBP":
            result = float( convert_number / 1.159357 )

        elif currency_from == "USD" and currency_to == "EUR":
            result = float( convert_number / 1.120236 )

        elif currency_from == "USD" and currency_to == "GBP":
            result = float( convert_number / 1.298628 )

        elif currency_from == "GBP" and currency_to == "EUR":
            result = float( convert_number * 1.159175 )

        elif currency_from == "GBP" and currency_to == "USD":
            result = float( convert_number * 1.298510 )

        else:
            result = "Pleae choose a different currencies!"

        params = { "result": result }

        return self.render_template( "result.html", params=params )



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route("/result", ConvertHandler)
], debug=True)
