<p>{{title}}</p>
<table border="1">
  %for val in values:
    % val = val[0] # get our JSON object out of the list
    <td>{{val}}</td>
  %end
%end
</table>
