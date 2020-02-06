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
    <div class="container">
        <h1>Current route name is: {{route_name}} </h1>

        <div class="row"><div class="col-12">
            % some_row = list(map(lambda x: x[0], timetable[0]))
            <table class="table table-dark table-hover">
                <thead>
                <tr>
                    <th scope="col">#</th>
                    % for title in some_row:
                        <th scope="col">{{title}}</th>
                    % end
                </tr>
                </thead>

                <tbody>
                    % for i, row in enumerate(timetable):
                        <tr>
                            <th scope="row">{{i}}</th>
                            % for col in row:
                                <td>{{col[1]}}</td>
                            % end
                        </tr>
                    % end
                </tbody>
            </table>
        </div></div>
    </div>
</body>
</html>