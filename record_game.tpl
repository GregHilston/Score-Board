<div class="container">
  <h2>Record a Win</h2>
    <form action="/record" method="post" id="recordForm">
      Game
      <select name="game" id="game">
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
      <input type="submit" value="Submit" id="submit">
    </form>
</div>

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script>
  $(function() {
    $("#recordForm").on("submit", function(e) {
      e.preventDefault();
      var selectedGame = $('#game').find(":selected").text();
      $.ajax({
        url: $(this).attr("action"),
        type: 'POST',
        data: $(this).serialize(),
        beforeSend: function() {
          console.log(selectedGame)
          console.log("Sending record for " + selectedGame +" ...")
          $("#message").html("sending...");
        },
        success: function(data) {
          console.log("Record successfully sent")
          $("#message").hide();
          $("#response").html(data);

          var wrapper = $('.reloadable-' + selectedGame);
          wrapper.load('#response .reloadable-' + selectedGame, function() {
             wrapper.children('.reloadable-' + selectedGame).unwrap();
          });
        }
      });
    });
  });
</script>