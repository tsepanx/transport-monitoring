%d = [
%    {'expected': '123', 'actual': '234'},
%    {'expected': '456', 'actual': '789'}
%]
<h1>Bus number is {{routeNumber}} and stop id is {{stopId}} </h1>
<table border = "100" bgcolor = "#F0F0F0" bordercolor = "green">
    <tr>
        <td> <h4>estimated time</h4> </td>
        <td> <h4> db time </h4> </td>
    </tr>
%for dic in d:
    <tr>
        <td> {{str(dic['expected'])}} </td>
        <td> {{str(dic['actual'])}} </td>
    </tr>
% end
</table>
