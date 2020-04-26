class Filter:
    def __init__(self, way_filter=None, week_filter=None):
        self.ways = ("AB", "BA")
        self.days = ("1111100", "0000011")

        if isinstance(way_filter, str):
            self.way_filter = [way_filter]
        else:
            self.way_filter = self.ways if way_filter is None else [self.ways[way_filter]]

        if isinstance(week_filter, str):
            self.week_filter = [week_filter]
        else:
            self.week_filter = self.days if week_filter is None else [self.days[week_filter]]


