<html>
<head>
    <meta charset="utf-8">
    <title>Records</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

    <link rel="stylesheet" href="/static/bootstrap.css" type="text/css">
    <link rel="stylesheet" href="/static/style.css" type="text/css">
    <script src="https://code.jquery.com/jquery-3.4.1.min.js" type = "text/javascript"></script>
    <script src="/static/bootstrap.js" type = "text/javascript"></script>
</head>
<body>
    <div class="container">
        <div class="row"><div class="col-12">
            <table class="table table-dark table-hover table-responsible">
                % titles = list(map(lambda x: x[0], records[0]))
                <thead><tr>
                    <th scope="col">#</th>
                    % for title in titles:
                        <th scope="col">{{title}}</th>
                    % end
                </tr></thead>
                <tbody>
                    % for i, stop in enumerate(records):
                        <tr>
                            <th scope="row">{{i + 1}}</th>
                            % for col in stop:
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