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
 
            <h1 class="allclear">Type feedback here.</h1>
            <p>Please include necessary steps to replicate any issues, <br>
            and your name or email if you wish to be contacted.</p>
            
            <form method="POST" action="/feedback">
                <textarea name="feedbacktext" type="text" class="feedbackbox"></textarea>
 				<button type="submit" class="submitfeedback">Submit</button>
              </form>
            <h6 class="jason blackplz">Designed by Jason in London</h6>
        </body>
</html>