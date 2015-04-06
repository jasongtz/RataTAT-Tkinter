
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{{apptitle}}</title>
        <link rel="stylesheet" href="static/css/normalize.css">
        <link rel="stylesheet" href="static/css/main.css">
        <meta name="viewport" content="width=device-width">
    </head>
        <body>
            <h1 class="logo"><p>R<span>T</span></p></h1>
            <h2 class="title">{{apptitle}}</h2>
            <p>{{genius}}</p>
            
                <div>
           		<form action="/genius1" method="GET" class="addbatt one">
                	<input type="submit" value="1">
                </form>
				<form action="/genius2" method="GET" class="addbatt two">
                	<input type="submit" value="2">
                </form>
                <form action="/genius3" method="GET" class="addbatt three">
                	<input type="submit" value="3">
                </form>
                </div>
               
            <br>
            
            <form action="/dc" method="GET">
                	<input type="submit" class="calibration" value="Awaiting Calibration">
                </form>
                
                <form action="/df" method="GET">
                	<input type="submit" class="failed" value="Display Failed">
                </form>
                
                <div>
                <form action="/nd" method="GET" class="display">
                	<input type="submit" class="display" value="Display RFP">
                </form>

                <form action="/nb" method="GET" class="battery">
                	<input type="submit" class="battery" value="Battery RFP">
                </form>
                </div>
        
            
            <h1 class="allclear">{{to_print}}</h1>
	        <p>{{!status}}</p>
	                    
            <div class="buttonrow2">
                <form action="/gr" method="GET" class="refreshstatus">
                	<input type="submit" value="Refresh Status">
                </form>
          
                
              </div>
                
            
             <div>  
             <form action="/feedback" method="GET" class="submitfeedback">
                	<input type="submit" value="Submit App Feedback">
			</form>
            </div> 

			 <h6 class="grjason">Designed by Jason in London</h6>
        </body>
</html>