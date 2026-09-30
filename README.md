# Dining brief

A one-page daily menu for Arrillaga, Wilbur, Lakeside, and Florence Moore.
A scheduled job pulls the menus from Stanford R&DE each morning and publishes a static page.

## Set up (about 5 minutes)

1. On GitHub, create a new repository (public; free accounts need this for Pages).
2. Upload everything in this folder, including the hidden `.github` folder, to the `main` branch.
3. In the repo, go to Settings, then Pages, and set Source to **GitHub Actions**.
4. Go to the Actions tab, open **Daily dining brief**, and click **Run workflow**.
5. When it finishes (about 2 minutes), your page is live at `https://<your-username>.github.io/<repo-name>/`. Bookmark it.

After that it refreshes itself every day around 5:30 am Pacific, so it's ready before 7.

## How dishes are sorted

Stanford's menu data has no station info, so `classify.py` sorts dishes with two signals: the first two dishes on
lunch and dinner menus are the day's headline mains, and keywords in dish names (chicken, tofu, broccoli, and so on)
place everything else into Mains, More protein, Veggies, or Sides and extras. It also flags steak dishes. If a dish
lands in the wrong section, add or remove a keyword in `classify.py`.

## Highlights

Visitors pick the foods they care about in the **Highlights** section (tap "Choose foods"). There are about 16 options
in two groups: Dishes (steak, pizza, fried chicken, pasta, seafood, and more) and Cuisines (Korean, Japanese, Mexican,
and more). Their picks are remembered in their browser, and the page then shows:

- a short summary sentence at the top ("Today: Korean at Florence Moore tonight; Next up: Steak on Thursday"),
- a row of tappable chips for each pick, showing which days and halls have it,
- a small tag on matching dishes and on the halls that serve them.

The first visit starts with Steak, Korean, and Pho at Wilbur selected.

To add, rename, or remove options, edit the list in `highlights.py`. Each entry is a name, a short tag, and a pattern
matched against dish names. Everyday standing items (the burger bar, grilled chicken, and so on) are ignored so that
highlights point at specials.

Pho is a special case: Wilbur's pho station doesn't appear on Stanford's menu site, so the page can't confirm it.
It shows dashed "unconfirmed" days based on the Mon, Wed, Fri schedule reported in fall 2025, which may change.

## Change the halls

Edit `HALLS` at the top of `scrape.py`. Available values:
Arrillaga, Branner, EVGR, FlorenceMoore, GerhardCasper, Lakeside, Ricker, Stern, Wilbur.

## Try it locally

    pip install -r requirements.txt
    python scrape.py        # fetches 7 days of menus into menus.json
    python render.py        # builds site/index.html
    open site/index.html

## Good to know

- GitHub pauses scheduled jobs on repos with no activity for 60 days. If the page stops updating, open the Actions tab and re-enable the workflow.
- The scraper reads Stanford's public menu page and pauses between requests. If Stanford changes that page, `scrape.py` will need a small update. The job refuses to publish an empty page, so a failure leaves yesterday's page in place.
