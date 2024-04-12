import * as React from "react";
import { Helmet } from "react-helmet";
import { useLoaderData } from "react-router-dom";

export default function Info() {
  const loaderData = useLoaderData() as { user: ListenBrainzUser };
  const userName = loaderData.user.name;
  return (
    <>
      <Helmet>
        <title>{`User - ${userName}`}</title>
      </Helmet>
      <div style={{ marginTop: "20px" }}>
        <p>
          The recordings shown in the next tab have been generated by a
          collaborative filtering algorithm using your past listening history.
          This page is mostly intended to be a debugging page, which is why it
          isn&apos;t linked from our pages. At the moment we have the following
          recommended tracks available:
          <ul>
            <li>
              <b>Raw recommendations: </b>These recordings are selected because
              they are unfiltered and similar to your listened recordings.
            </li>
          </ul>
        </p>
      </div>

      <p>
        The sets of recordings above are sorted on the score that was assigned
        by the collaborative filtering algorithm; a higher score indicates a
        greater likeliness that you would like this selected track, at least in
        theory. For more information about this work and how to give us feedback
        on these recordings, visit the{" "}
        <a href="https://community.metabrainz.org/t/tracks-that-you-might-like/495812">
          MetaBrainz Community Discourse site
        </a>
      </p>
    </>
  );
}
