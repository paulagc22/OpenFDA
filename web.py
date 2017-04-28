#Copyright [2017] [Paula González Carrasco]

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.








import http.server
import socketserver
import http.client
import json


#HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    OPENFDA_API_URL= 'api.fda.gov'
    OPENFDA_API_EVENT = '/drug/event.json'
    OPENFDA_API_DRUG='?search=patient.drug.medicinalproduct:'
    OPENFDA_API_COMPANY='?search=companynumb:'

    def get_event(self):
        ##
        #GET EVENt
        ##
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10")
        r1=conn.getresponse()
        data1 = r1.read()
        data1=data1.decode('utf8')
        biblioteca_data1=json.loads(data1)
        results=biblioteca_data1['results']
        return results

    def get_event_drug(self,drug):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + self.OPENFDA_API_DRUG + drug +"&limit=10")
        r1=conn.getresponse()
        data1 = r1.read()
        data1=data1.decode('utf8')

        return data1

    def get_event_companies(self,companies):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + self.OPENFDA_API_COMPANY + companies +"&limit=10")
        r1=conn.getresponse()
        data1 = r1.read()
        data1=data1.decode('utf8')

        return data1



    def get_drugs(self,results):
        events=[]
        for event in results:
            patient=event['patient']
            drug=patient ['drug']
            medicinalproduct=drug[0]['medicinalproduct']
            events+=[medicinalproduct]
        return events

    def get_companies (self,results):
        events=[]
        for event in results:
            events += [event['companynumb']]
        return events

    def search_companies (self,data1):
        companies1=[]
        data=data1
        biblioteca_data=json.loads(data)
        search_companies_results= biblioteca_data['results']
        for event in search_companies_results:
            patient=event['patient']
            drug=patient ['drug']
            companies1+= [drug[0]['medicinalproduct']]
        return companies1

    def search_drug(self,data1):
       companies=[]
       data=data1
       biblioteca_data=json.loads(data)
       search_drug_results=biblioteca_data['results']
       for event in search_drug_results:
           companies += [event['companynumb']]
       return companies

    def get_main_page(self):
        #envia mensajes de vuelta al cliente

        html = """
        <html>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <form method="get" action="listDrugs">
                    <input type = "submit" value="Enviar OpenFDA">
                    </input>
                </form>
                <form method="get" action="listCompanies">
                    <input type = "submit" value="COMPANIES">
                    </input>
                </form>

                <form method="get" action="searchDrug">
                    <input type= "submit" value="Enviar drug"></input>
                    <input type="text" name="drug">
                    </input>
                </form>
                <form method="get" action="searchCompany">
                    <input type= "submit" value="Enviar companies"></input>
                    <input type="text" name="company">
                    </input>
                </form>
            </body>
        </html>
        """
        return html

    def get_second_page(self,drugs):
        drugs_html= """
        <html>
           <head>
               <title>OpenFDA Cool App</title>
           </head>
           <body>
               <ul>
        """

        for drug in drugs:
            drugs_html+='<li>' + drug + '</li>'

        drugs_html+="""
               </ul>
           </body>
        </html>
        """
        return drugs_html

    #GET
    def do_GET(self):
        main_page=False
        is_event=False
        is_drug= False
        is_companies_event=False
        is_companies=False
        if self.path=='/':
            main_page= True
        elif 'listDrugs' in self.path:
            is_event=True
        elif 'searchDrug' in self.path :
            is_drug= True
        elif 'listCompanies' in self.path:
            is_companies_event=True
        elif 'searchCompany' in self.path:
            is_companies=True

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        html=self.get_main_page()

        if main_page:
            self.wfile.write(bytes(html, "utf8"))
        elif is_event:
            event=self.get_event()
            drugs= self.get_drugs(event)
            html=self.get_second_page(drugs)
            self.wfile.write(bytes(html, "utf8"))
        elif is_drug:
            drug=self.path.split('=')[1]
            event=self.get_event_drug(drug)
            companynumb=self.search_drug(event)
            html2=self.get_second_page(companynumb)
            self.wfile.write(bytes(html2, 'utf8'))
        elif is_companies_event:
            event=self.get_event()
            companies= self.get_companies(event)
            html=self.get_second_page(companies)
            self.wfile.write(bytes(html, "utf8"))

        elif is_companies:
            companies=self.path.split('=')[1]
            event=self.get_event_companies(companies)
            companynumb=self.search_companies(event)
            html2=self.get_second_page(companynumb)
            self.wfile.write(bytes(html2, 'utf8'))



        return
