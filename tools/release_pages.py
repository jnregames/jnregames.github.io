"""Static release marketing: shared configuration, no browser JavaScript."""
import html
import json
import re


def build_release_pages(root, base):
    release = json.loads((root / 'content/release.json').read_text())
    assert release['status'] in ('coming_soon', 'available_now')
    upcoming = release['status'] == 'coming_soon'
    version = html.escape(release['version'])
    slug = release['version'].replace('.', '-')
    for lang in ('en', 'es'):
        es = lang == 'es'
        home = '/es/' if es else '/'
        route = f'{home}galaxiga/updates/{slug}/'
        other = f'{"/" if es else "/es/"}galaxiga/updates/{slug}/'
        file = root / ('es/index.html' if es else 'index.html')
        page = file.read_text()
        title = html.escape(release['title'][lang])
        status = ('PRÓXIMAMENTE' if es else 'COMING SOON') if upcoming else ('YA DISPONIBLE' if es else 'AVAILABLE NOW')
        download = 'JUGAR A GALAXIGA RETRO' if es else 'PLAY GALAXIGA RETRO'
        store = html.escape(release['download_url'], quote=True)
        note = (f'La versión {release["current_version"]} está disponible en Google Play. La {version} sigue en desarrollo; las funciones pueden cambiar.' if es else f'Version {release["current_version"]} is available on Google Play. {version} is in development; features may change.') if upcoming else (f'La versión {version} está disponible en Google Play.' if es else f'Version {version} is available on Google Play.')
        if release['release_date']:
            note += ' ' + ('Fecha de lanzamiento: ' if es else 'Release date: ') + html.escape(release['release_date']) + '.'
        intro = ('Galaxiga Retro evoluciona. La próxima actualización amplía la personalización de naves, transforma las formaciones enemigas y renueva la presentación del combate, con más motivos para volver a la batalla.' if es else 'Galaxiga Retro is evolving. Our upcoming update brings expanded ship customization, more dynamic enemy formations, improved combat presentation, and new reasons to return to the fight.') if upcoming else ('Descubre las novedades de Galaxiga Retro.' if es else 'Discover what’s new in Galaxiga Retro.')
        detail = 'Explorar la actualización' if es else 'Explore the update'
        artnote = 'Vista de desarrollo: diseños cosméticos reales; no es una captura de combate.' if es else 'Development art preview: actual cosmetic designs, not a combat screenshot.'
        banner = f'''<section class="release-announcement shell" id="update" aria-labelledby="release-title"><div class="release-topline"><span class="status">{version} {status}</span><span class="eyebrow">{'PRÓXIMA MISIÓN' if es else 'NEXT MISSION'} / {version}</span></div><div class="release-grid"><div><p class="eyebrow">GALAXIGA RETRO {version}</p><h2 id="release-title">{title}</h2><p class="section-intro">{intro}</p><div class="actions"><a class="button secondary" href="{route}">{detail} ↗</a><a class="text-link" href="{store}">{download} ↗</a></div><p class="disclosure">{note}</p></div><figure class="fleet-art"><img src="/assets/update-showcase.webp" width="1200" height="520" alt="{'Naves con alas, blindajes y adornos cosméticos en desarrollo.' if es else 'Development ship renders with cosmetic wings, armor and attachments.'}" fetchpriority="high"><figcaption>{artnote}</figcaption></figure></div></section>'''
        # Replace the previous unversioned update and promote it above the game hero.
        page = re.sub(r'<section class="section shell" id="update">.*?</section>', '', page, flags=re.S)
        page = page.replace('<main id="main">', '<main id="main">'+banner)
        page = page.replace('<a class="language"', f'<a class="update-nav" href="{route}">{version}</a><a class="language"', 1)
        oldtitle = re.search(r'<title>(.*?)</title>', page)[1]
        newtitle = f'Galaxiga Retro {version} — {title} | {status}'
        desc = (f'Galaxiga Retro {version}: {title}, {status.lower()}. Personalización de naves, nuevas formaciones y botín. Juega a la versión actual en Android.' if es else f'Galaxiga Retro {version} — {title}, {status.lower()}. Preview ship customization, enemy formations and boss loot. Play the current Android release.')
        page = page.replace(oldtitle, newtitle)
        page = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m:m[1]+desc, page)
        page = page.replace('/assets/key-art.webp"><meta property="og:image:width" content="1024"><meta property="og:image:height" content="500">', '/assets/update-social.webp"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">')
        page = page.replace('Get it on Google Play', download).replace('Descargar en Google Play', download)
        file.write_text(page)
        labels = ['PERSONALIZACIÓN','COMBATE','BOTÍN Y RECOMPENSAS','MEJORAS VISUALES'] if es else ['SHIP CUSTOMIZATION','COMBAT IMPROVEMENTS','LOOT & REWARDS','VISUAL IMPROVEMENTS']
        features = ''
        for i, f in enumerate(release['features']):
            assert f['availability'] in ('planned', 'awaiting_production_validation', 'verified')
            confirmed = not upcoming and f['availability'] == 'verified'
            state = ('INCLUIDO EN' if es else 'INCLUDED IN') if confirmed else ('PREVISTO PARA' if es else 'PLANNED FOR')
            features += f'<article id="{f["id"]}"><p class="eyebrow">0{i+1} / {labels[i]}</p><h3>{html.escape(f["title"][lang])}</h3><p>{html.escape(f["body"][lang])}</p><span class="feature-state">{state} {version}</span></article>'
        captions = ['Hangar: alas y blindajes cosméticos','Formaciones: movimiento de reloj','Botín: presentación de recompensas'] if es else ['Hangar: cosmetic wings and armor','Formations: clockwork movement','Loot: reward presentation']
        alts = ['Pantalla de cosméticos con una nave equipada con Wing Fins.','Enemigos organizados en una formación hexagonal.','Revelación de botín de jefe con monedas y componentes.'] if es else ['Cosmetics screen showing a ship equipped with Wing Fins.','Enemy ships arranged in a hexagonal formation.','Boss loot reveal showing coins and components.']
        gallery = ''.join(f'<figure><a href="/assets/{img}.webp" aria-label="{alt}"><img src="/assets/{img}.webp" width="720" height="{height}" alt="{alt}" loading="lazy"></a><figcaption>{caption}</figcaption></figure>' for img,caption,alt,height in zip(['update-hangar-es' if es else 'update-hangar','update-combat','update-loot'],captions,alts,[1280,1440,1440]))
        returning = '¿Ya defiendes la galaxia?' if es else 'Already defending the galaxy?'
        returncopy = 'Tu próxima misión será más grande. Más personalización, nuevos encuentros y más recompensas están en camino.' if es else 'Your next mission is getting bigger. More customization, fresh combat encounters, and expanded rewards are on the way.'
        if not upcoming:
            returncopy = 'Descubre más personalización, nuevos encuentros y recompensas.' if es else 'Discover more customization, fresh encounters and rewards.'
        previewnote = 'Capturas reales de desarrollo en Unity. Interfaz, precios, recompensas y equilibrio sujetos a cambios; no muestran la versión actual de Google Play.' if es else 'Actual Unity development captures. UI, prices, rewards and balance may change; these do not show the current Google Play release.'
        body = f'''<main id="main"><section class="release-hero shell"><a class="text-link" href="{home}">← {'Volver al juego' if es else 'Back to the game'}</a><p class="eyebrow">GALAXIGA RETRO {version}</p><h1>{title}</h1><p class="status">{version} {status}</p><p class="lead">{intro}</p><div class="actions"><a class="button primary" href="{store}">{download} ↗</a><a class="text-link" href="#features">{'Ver las novedades' if es else ('See what’s coming' if upcoming else 'Explore the features')} ↓</a></div><p class="disclosure">{note}</p><figure class="fleet-art"><img src="/assets/update-fleet.webp" width="1600" height="582" alt="{'Vista de naves con accesorios cosméticos en desarrollo.' if es else 'Development preview of ships wearing cosmetic attachments.'}"><figcaption>{artnote}</figcaption></figure></section><section class="section shell" id="features"><p class="eyebrow">{'EL PRÓXIMO CAPÍTULO' if es else 'THE NEXT CHAPTER'}</p><h2>{'Más estilo. Más combate.' if es else 'More identity. More action.'}</h2><div class="release-features">{features}</div></section><section class="section shell"><h2>{'Desde el hangar hasta la batalla' if es else 'From the Hangar to the front line'}</h2><p class="section-intro">{previewnote}</p><div class="gallery release-gallery">{gallery}</div></section><section class="section shell"><div class="update"><p class="eyebrow">{'PARA PILOTOS VETERANOS' if es else 'FOR RETURNING PILOTS'}</p><h2>{returning}</h2><p>{returncopy}</p><p class="disclosure">{note}</p><a class="button primary" href="{store}">{download} ↗</a></div></section></main>'''
        head = page.split('<main id="main">')[0]
        head = head.replace(f'href="{base}{home}"', f'href="{base}{route}"', 1)
        head = re.sub(r'<link rel="alternate".*?hreflang="x-default"[^>]*>', f'<link rel="alternate" hreflang="en" href="{base}/galaxiga/updates/{slug}/"><link rel="alternate" hreflang="es" href="{base}/es/galaxiga/updates/{slug}/"><link rel="alternate" hreflang="x-default" href="{base}/galaxiga/updates/{slug}/">', head)
        head = head.replace(f'property="og:url" content="{base}{home}"', f'property="og:url" content="{base}{route}"')
        head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
        head = head.replace('href="#game"', f'href="{home}#game"').replace('href="#preview"', f'href="{home}#preview"')
        head = re.sub(r'(class="language" href=")[^"]*', lambda m:m[1]+other, head)
        footer = '<footer'+page.split('<footer',1)[1]
        target = root / route.strip('/') / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(head+body+footer)
    urls = ['/', '/es/', f'/galaxiga/updates/{slug}/', f'/es/galaxiga/updates/{slug}/']
    (root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{base}{u}</loc></url>\n' for u in urls)+'</urlset>\n')
