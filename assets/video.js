// Keep YouTube disconnected until the visitor explicitly loads its player.
document.querySelectorAll('[data-youtube]').forEach(preview => {
  preview.addEventListener('click', event => {
    event.preventDefault();
    const player = document.createElement('iframe');
    player.src = `https://www.youtube-nocookie.com/embed/${preview.dataset.youtube}`;
    player.title = 'Galaxiga Retro — Boss Rematches, Lasers & Mining | Upcoming Update';
    player.allow = 'encrypted-media; picture-in-picture; fullscreen';
    player.allowFullscreen = true;
    player.referrerPolicy = 'strict-origin-when-cross-origin';
    preview.replaceWith(player);
    player.focus();
  });
});
