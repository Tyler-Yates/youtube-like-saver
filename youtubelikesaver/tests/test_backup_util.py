import os

from youtubelikesaver.src.backup_util import BackupUtil, BACKUP_SUBFOLDER

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=7_cDT5_Vmdc"
TEST_VIDEO_TITLE = "defective weaponry"


class TestBackupUtil:
    def test_save_audio_and_video(self, tmpdir):
        backup_util = BackupUtil(tmpdir)
        backup_util.save_audio_and_video(TEST_VIDEO_URL)

        listdir = os.listdir(tmpdir)
        assert "completed.txt" in listdir

        listdir = os.listdir(os.path.join(tmpdir, BACKUP_SUBFOLDER))
        assert ("%s.m4a" % TEST_VIDEO_TITLE) in listdir
        assert ("%s.mkv" % TEST_VIDEO_TITLE) in listdir
        assert ("%s.webp" % TEST_VIDEO_TITLE) in listdir
