def display_loading(loading):
    loading.markdown("""
        <section>
            <div class="loader"></div>
        </section>
    """, unsafe_allow_html=True)


def hide_loading(loading):
    loading.empty()


def model_used(model):
    return f"""
        <div class='whole_sidebar'>
           <div class='used_model'>
               <label>Used model : </label>
               <p>{model}</p>
           </div>
        </div>
        """


def make_divs(requests_x):
    if len(requests_x) == 0:
        return """ <h5 class="card-title" style="color:white;margin-top:6svh; text-align:left;margin-left:2%;">No requests found for the applied filters</h5>"""

    html_divs_x = ""
    for x, request_i in enumerate(requests_x):
        header_x = f"heading-{x}"
        collapse_x = f"collapse-{x}"
        color = "green" if request_i['label_predicted'] == 'Benign' else "red"
        html_divs_x += f"""
            <div id="card_con" class="card" style='border: 1px solid {color}!important'>
                <div class="card-header" id={header_x} >
                    <div class="w-100" style="display: flex; justify-content: space-between; align-items: baseline;">
                        <button class="btn btn-link" data-toggle="collapse" data-target="#{collapse_x}" aria-expanded="true" aria-controls="{collapse_x}">
                          <p>Request N:{request_i['request_id']}</p>
                        </button>
                        <label style="padding:3px; padding-left: 8px; padding-right: 8px; background-color: #2C2C38; border-radius: .5em;color:white">
                            {request_i['label_predicted']}
                        </label>
                    </div>
                    <div style="display: flex; justify-content: end">
                        <span class="value" style="text-align: left; color: green">{request_i['timestamp']}</span>
                    </div>
                </div>
                <div id="{collapse_x}" class="collapse" aria-labelledby="{header_x}" data-parent="#accordion">
                  <div class="card-body">
                    <div class="row" style="display:flex; justify-content: space-between">
                        <div class="col">
                            <p style="display:flex; justify-content: space-between">
                                <span class="label" style="text-align: left">FlDuration</span> 
                                <span class="value" style="text-align: left">{request_i['flow_duration']}</span>
                            </p>
                            <p style="display:flex; justify-content: space-between">
                                <span class="label" style="text-align: left">Rate</span> 
                                <span class="value" style="text-align: left">{request_i['rate']}</span>
                            </p>
                            <p style="display:flex; justify-content: space-between">
                                <span class="label" style="text-align: left">Drate</span> 
                                <span class="value" style="text-align: left">{request_i['drate']}</span>
                            </p>
                        </div>
                        <div class="col-auto d-none d-md-block separator">
                            <div class="line"></div>
                        </div>
                        <div class="col" style="">
                            <p style="display:flex; justify-content: space-between">
                                <span class="label" style="text-align: left">Duration</span> 
                                <span class="value" style="text-align: left">{request_i['duration']}</span>
                            </p>
                            <p style="display:flex; justify-content: space-between">
                                <span class="label" style="text-align: left">Srate</span> 
                                <span class="value" style="text-align: left">{request_i['srate']}</span>
                            </p>
                            <p style="display:flex; justify-content: space-between">
                                <span class="label" style="text-align: left">Magnitude</span> 
                                <span class="value" style="text-align: left">{request_i['Magnitue']}</span>
                            </p>
                        </div>
                    </div>
                  </div>
                </div>
            </div>
        """
    return html_divs_x


def make_frame(html_iframe_y):
    return f"""
        <style>

            /* ===== Scrollbar CSS ===== */
              /* Firefox */
              * {{
                scrollbar-width: thin;
                scrollbar-color: white #2C2C38;
              }}

              /* Chrome, Edge, and Safari */
              *::-webkit-scrollbar {{
                width: 10px;
              }}

              *::-webkit-scrollbar-track {{
                background: #2C2C38;
              }}

              *::-webkit-scrollbar-thumb {{
                background-color: #dad7da;
                border-radius: 10px;
                border: 10px solid #ffffff;
              }}

            :root {{ background-color: #2C2C38; }}
            #accordion {{ background-color: #2C2C38; padding-left: 0px; padding-right: 15px; }}
            #card_con {{ background-color: #262730; margin-bottom: 10px; border: 1px solid green; border-radius: 0.5em; }}
            .card-body {{ color: white!important; }}
            .btn-link {{ color: white!important; }}

            .separator {{ 
                margin: 10px auto;
                width: 60%;
                height: 100px;
                position:relative;
                text-align:center
                background-color: green;
            }}

            .line {{
                width: 1px;
                height: 100%;
                border-right: 2px solid;
                border-image: linear-gradient(transparent, green, transparent) 40;
            }}


        </style>

        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <div id="accordion">
          {html_iframe_y}
        </div>
    """


def whole_page_css():
    return """
        <style>

            .st-emotion-cache-uf99v8 {
                overflow: hidden;
            }

            [data-testid="stIFrame"] {
                padding: 10px!important;
            }

            [data-testid="stHeader"]{
                display: none;
            }

            [data-testid="stAppViewContainer"]{
                background-color: #2C2C38;
            }
            
            .main {
                padding-top: 12svh;
            }

            [data-testid="stAppViewBlockContainer"]{
                padding-top: 0px;
            }

            .st-emotion-cache-1y4p8pa {
                max-width: 90%;   
            }


            [data-testid="stSidebarContent"]{
                background-color: #1B1B21;
                padding: 0!important;
                border-right: 2px solid;
                border-image: linear-gradient(transparent, green, transparent) 40;
            }

            [data-testid="stSidebarContent"] button[kind="secondary"]{
                position: absolute;
                top: 10svh;
                left: 0;
                background-color: transparent!important;
                color: white!important;
                border: 2px solid green!important;
            }

            [data-testid="stSidebarContent"] button[kind="secondary"]:hover{
                background-color: green!important;
                color: white!important;
                border: 2px solid green!important;
            }

            [data-testid="stSidebarContent"] button[kind="secondary"]:focus{
                background-color: green;
                border: 1px solid black;
            }


            button[kind="primary"]{
                position: relative;
                top: 5svh;
                background-color: transparent!important;
                color: white!important;
                border: 2px solid green!important;
            }

            button[kind="primary"]:hover{
                background-color: green!important;
                color: white!important;
                border: 2px solid green!important;
            }

            button[kind="primary"]:focus{
                background-color: green;
                border: 1px solid black;
            }


            [data-testid="stSidebarUserContent"]{
                padding: 0px;
                padding-top: 2vh;
                padding-left: 2vw;
                padding-right: 2vw;
            }

            [data-testid="stMarkdownContainer"] h1{
                text-align: center
            }

            .used_model {
                display: flex;
                justify-content: space-around;
                align-items: baseline;
            }

            .used_model label{
            }

            .used_model p{
                border: 2px solid green;
                border-radius: 0.7em;
                padding: 0.5em;
            }

            .whole_sidebar{
                height: 10svh;
            }

            .counts_container {

                display: flex;
                flex-direction: column;
                gap: 1em;
                justify-content: space-around;
                align-items: left;
                margin-top: 20px;
            }

             h3.count_container {
                background-color: #2C2C38;
                border-radius: .5em .5em 0 0;
                width: 100%;
                height: 5vh;
                padding-left: 10%;
                text-align: left;
                margin-bottom: 0;
            }

            p:has(code) {
                background-color: #2C2C38;
                border-radius: 0 0 .5em .5em ;
                width: 100%!important;
                text-align: left;
                font-size: 30px!important;
                padding-left: 8%;
                padding-top: 0;
            }

            code {
                background-color: #2C2C38;
                color: white;
            }

            .count_container h2{
                color: white;
                text-align: left;
                height: 3vh;
                font-weight: bold;
                opacity: 0.7;
            }

            .count_container label{
                text-align: left;
                font-size: 2.5em;
                height: 10vh;
            }



            .bottom button{

                background-color: green;
                border: none;
                border-radius: 0.4em;
                padding: 0.5em 1em;
                color: white;
                border: 2px solid grey;
                box-shadow: 2px 2px 5px 2px black;
                font-weight: bold;
            }
            
            section {
                width: 100%;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .loader {
                width: 80px;
                height: 80px;
                border: transparent solid 3px;
                border-left-color: green;
                border-top-color: green;
                border-radius: 100%;
                position: relative;
                animation: loading 4s infinite linear;
                
            }
    
            .loader::before {
                position: absolute;
                content: '';
                top: 10px;
                left: 10px;
                right: 10px;
                bottom: 10px;
                border: transparent solid 3px;
                border-left-color: green;
                border-top-color: green;
                border-radius: 100%;
                animation: loading 1s infinite linear reverse
            }
    
    
            .loader::after {
                position: absolute;
                content: '';
                top: 20px;
                left: 20px;
                right: 20px;
                bottom: 20px;
                border: transparent solid 3px;
                border-left-color: green;
                border-top-color: green;
                border-radius: 100%;
                animation: loading 3s infinite linear;
            }
    
            @keyframes loading {
                from {
                    transform: rotate(0deg);
                }
    
                to {
                    transform: rotate(360deg);
                }
            }

        </style>
        """
