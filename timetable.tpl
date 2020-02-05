<h1>Current route name is: {{route_number}} </h1>
<table border=3px bgcolor="#F0F0F0" bordercolor="green">
    <tr>
        <td> <h4>db time</h4> </td>
        <td> <h4> estimated time </h4> </td>
    </tr>
%for row in timetable:
    <tr>
        <td> {{str(dic['expected'])}}  </td>
    </tr>
% end
</table>
