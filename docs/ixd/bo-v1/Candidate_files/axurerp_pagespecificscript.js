
var PageName = 'Candidate';
var PageId = 'p91a1de43f8b34e9c919d5af5bd25897a'
var PageUrl = 'Candidate.html'
document.title = 'Candidate';

if (top.location != self.location)
{
	if (parent.HandleMainFrameChanged) {
		parent.HandleMainFrameChanged();
	}
}

if (window.OnLoad) OnLoad();
