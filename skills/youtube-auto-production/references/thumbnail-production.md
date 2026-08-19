# Thumbnail production

Use this reference only when a video needs thumbnails.

## Required inputs

- locked narration and its first 30 seconds;
- intended audience and one credible promise;
- the main mechanism shown in the video;
- any authorized presenter reference;
- exact Korean headline copy.

## A/B logic

- A — attainable outcome: make the viewer feel “I could start this too.”
- B — repeatable mechanism: make the process concrete with time, steps, or system.

Change the promise and composition together only when testing two complete hypotheses. For a controlled live test, keep the title fixed while comparing thumbnails.

## Image-generation prompt contract

Specify 16:9 YouTube use, mobile readability, one expressive subject, one supporting mechanism, exact Korean text, high contrast, and negative constraints. Avoid guaranteed revenue, fake screenshots, platform logos, clutter, tiny copy, excessive glow, and misspelled Korean.

Use GPT Image 2 only through a locally supplied `OPENAI_API_KEY`; never store the key or generated request payload containing secrets in Git. Save the accepted bitmap and prompt in the repository.

After generation, inspect full size and a 320 px-wide preview. Reject text errors, cropped faces, deformed hands, or a promise unsupported by the video.
