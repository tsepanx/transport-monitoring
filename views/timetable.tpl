<html>
<head>
    <meta charset="utf-8">
    <title>{{route_name}}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

    <link rel="stylesheet" href="static/bootstrap.css" type="text/css">
    <link rel="stylesheet" href="static/style.css" type="text/css">
    <script src="https://code.jquery.com/jquery-3.4.1.min.js" type = "text/javascript"></script>
    <script src="static/bootstrap.js" type = "text/javascript"></script>
</head>
<body>
    <h1>Current route name is: {{route_name}} </h1>
    <table class="table table-dark">
    %for row in timetable:
        <tr>
            % for col in row:
                <td>{{col}}</td>
            % end
        </tr>
    % end
    </table>
</body>
</html>