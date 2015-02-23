from django.db import models

class Epoch(models.Model):
    epoch = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

class TenhouPlayer(models.Model):
    epoch = models.CharField(max_length=255)
    tenhou_name = models.CharField(max_length=255)
    primary_id = models.ForeignKey('TenhouPlayer', null=True)
    rank = models.CharField(max_length=255)
    rate = models.IntegerField()
    rank_time = models.DateTimeField()

    ngames = models.IntegerField(default=0)
    ndays = models.IntegerField(default=0)
    nplace1 = models.IntegerField(default=0)
    nplace2 = models.IntegerField(default=0)
    nplace3 = models.IntegerField(default=0)
    nplace4 = models.IntegerField(default=0)
    nmangan = models.IntegerField(default=0)
    nhaneman = models.IntegerField(default=0)
    nbaiman = models.IntegerField(default=0)
    nsanbaiman = models.IntegerField(default=0)
    nyakuman = models.IntegerField(default=0)

    class Meta:
        unique_together = ('epoch', 'tenhou_name')

    def __str__(self):
        return self.tenhou_name

    def placements(self):
        return "{} / {} / {} / {}".format(self.nplace1, self.nplace2, self.nplace3, self.nplace4)

    def place_avg(self):
        return (self.nplace1 + self.nplace2 * 2 + self.nplace3 * 3 + self.nplace4 * 4) / self.ngames

    def cp(self):
        return (self.nplace1 * 4 + self.nplace2 * 3 + self.nplace3 * 2 + self.nplace4)

    def cp_avg(self):
        return self.cp() / self.ngames

    def limits(self):
        bits = []
        for name, val in (
            ('man', self.nmangan),
            ('hane', self.nhaneman),
            ('bai', self.nbaiman),
            ('sanbai', self.nsanbaiman),
            ('yakuman', self.nyakuman),
            ):
            if val:
                bits.append("{} {}".format(val, name))
        return ', '.join(bits)

    def tp(self):
        return (self.nyakuman * 10 + self.nsanbaiman * 8 + self.nbaiman * 5 + self.nhaneman * 4 + self.nmangan * 3)

    def tp_avg(self):
        return self.tp() / self.ngames

    def sp(self):
        return self.cp() + self.tp()

    def sp_avg(self):
        return self.sp() / self.ngames

class TenhouGame(models.Model):
    game_id = models.CharField(max_length=255, unique=True)
    epoch = models.CharField(max_length=255)
    when_played = models.DateTimeField()
    lobby = models.IntegerField()
    players = models.ManyToManyField(TenhouPlayer)
    scores = models.CharField(max_length=255, blank=True)
    url_names = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.game_id
