import os

from sigil import _, api, fields, models
from sigil.tools import config

from .kplus_tools import extract_info, extract_lyrics


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

    status = fields.Selection([
        ("waiting", "Waiting"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ], default="waiting", required=True, readonly="true")

    # Auto Generated
    title = fields.Char(readonly=True)
    artist = fields.Char(readonly=True)
    duration = fields.Float(readonly=True)

    lyrics = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)
        for task in tasks:
            task.extract_info()
        return tasks

    @api.model
    def get_cookiepath(self):
        #TODO: Rotate cookiefile and populate cookiefile
        return os.path.join(config['data_dir'], "cookies.txt")
        
    def extract_info(self) -> None:
        title, artist, duration = extract_info(self.source_url, cookiefile=self.get_cookiepath())
        self.write({
            "title": title,
            "artist": artist,
            "duration": duration
        })
        if self.karaoke_type == "plus":
            self.write({
                "lyrics": extract_lyrics(self.title, self.artist, self.duration)
            })

    def action_refetch_info(self) -> None:
        return self.extract_info()

    # Task.run() will immediately run
    def action_run(self) -> None:
        """ Run the karaoke task immediately.

            This is intentionally the entry point from the UI.
            The actual processing lives in `_run()`,
            which can later be executed by a GPU worker.
        """
        pass
    # processjobs will be run on scheduled
    