<p>{{title}}</p>
<table border="1">
  %for val in values:
    % val = str(val).replace("[","")
    % val = str(val).replace("]","")
    % val = str(val).replace("'","")
    <td>{{val}}</td>
  %end
%end
</table>
