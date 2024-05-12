# helios-procedures
LaTeX source for HELIOS related procedures

To get the procedures, go to the [release page on right side](https://github.com/aris-space/helios-procedures/releases) and download it from the release assets.

## Usage

### Doing changes

Commit messages should follow [conventional commit message structure](https://www.conventionalcommits.org/)

TODO: examples

Changes should be small and atomic.
Basically make many small PRs rather than one big one.

⚠️ Note that the `main` branch is protected, all changes have to be made to new branches and then merged via a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) ⚠️

Whenenever there are unreleased changes on main, `tagpr` will create a new release pull request.
Merging that PR will automatically create a new release.

### Structure

All LaTeX source is located in `src/` and from there separated by subteam (`dacs-sw`, ...).
The `src/common/` folder contains shared content like assets.

### Other

By default, documents will have a draft watermark controlled by a single LaTeX variable unless they are compiled by the release pipeline.
