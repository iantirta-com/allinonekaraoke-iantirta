
from sigil import api, fields, models, _

class KaraokeKaraoke(models.Model):
    _name = 'karaoke.karaoke'
    _description = 'Karaoke Karaoke'

    source_url = fields.Char(required=True)
    karaoke_type = fields.Selection([
        ("basic", "Basic"),
        ("plus", "Plus (Lyrics Subtitle)"),
    ], required=True, string="Karaoke Generation Type")

    _unique_source_url = models.Constraint(
        "UNIQUE(source_url)",
        "The Source Url must be unique or this url have already in database."
    )

    # Auto Generated
    title = fields.Char(readonly=True)
    artist = fields.Char(readonly=True)
    duration = fields.Float(readonly=True)

    lyrics = fields.Text()

    # Helper
    _downloader = None

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)
        for task in tasks:
            task.extract_info()
        return tasks

    @api.model
    def get_cookiepath(self):
        pass
        
    @api.model
    def get_downloader(self):
        # Need Cookiefile
        pass

    def extract_info(self) -> None:
        # Needs cookiefile
        downloader = self._downloader or self.get_downloader()
        title, artist, duration = Downloader().extract_info(self.source_url)
        self.write({
            "title": title,
            "artist": artist,
            "duration": duration
        })

    # Task.run() will immediately run
    # processjobs will be run on scheduled
    