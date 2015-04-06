
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
                <form action="/confirmd" method="GET" class="adddis">
                	<input type="submit" value="Add Display">
                </form>

               <form action="/confirmb" method="GET" class="addbatt">
                	<input type="submit" value="Add Battery">
                </form>

                </div>
            
            <h1 class="allclear">{{to_print}}</h1>
	        <p>{{!status}}</p>
 			
            <div>
 			<form action="/bar" method="GET" class="refreshstatus">
                	<input type="submit" value="Refresh Status">
                </form>
           <form action="/feedback" method="GET" class="submitfeedback">
                	<input type="submit" value="Submit App Feedback">
			</form>
            </div>
            <h6 class="jason blackplz">Designed by Jason in London</h6>

        </body>
</html>