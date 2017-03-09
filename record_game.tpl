<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body>
    <div class="container">
      <h2>Record a Win</h2>
        <form action="/record" method="post">
          Game
          <select name="game">
              %for game in games:
              % game = game[0] # get our JSON object out of the list
              <option value="{{game}}">{{game}}</option>
              %end
          </select>

          Winner
          <select name="winner">
              %for player in players:
              % player = player[0] # get our JSON object out of the list
              <option value="{{player}}">{{player}}</option>
              %end
          </select>

          Loser
          <select name="loser">
              %for player in players:
              % player = player[0] # get our JSON object out of the list
              <option value="{{player}}">{{player}}</option>
              %end
          </select>
          <input type="submit" value="Submit">
        </form>
    </div>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  </body>
</html>