
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>RataTAT v0.2.1</title>
        <link rel="stylesheet" href="static/css/normalize.css">
        <link rel="stylesheet" href="static/css/main.css">
        <meta name="viewport" content="width=device-width">
    </head>
        <body>
            <h1 class="logo"><p>R<span>T</span></p></h1>
            <h2 class="title">{{apptitle}}</h2>
            <p>{{genius}}</p>
                
            <h1 class="allclear">{{to_print}}</h1>
            
            <div>
			<form action="/bar" method="GET" class="cancel">
    	      <input type="submit" value="Cancel">
        	</form>

		   <form action="/d" method="GET" class="bookin">
				<input type="submit" value="CONFIRM BOOK-IN">
			</form>
			</div>

          <h6 class="confirmjason">Designed by Jason in London</h6>
         </body>
</html>