<h1>Bus number is {{route_number}} and stop id is {{stop_id}} </h1>
<table border=5px bgcolor = "#F0F0F0" bordercolor = "green">
    <tr>
        <td> <h4>db time</h4> </td>
        <td> <h4> estimated time </h4> </td>
    </tr>
%for dic in web_info:
    <tr>
        <td> {{str(dic['expected'])}}  </td>
        <td> {{str(dic['actual'])}} </td>
    </tr>
% end
</table>
