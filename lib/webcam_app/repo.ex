defmodule WebcamApp.Repo do
  use Ecto.Repo,
    otp_app: :webcam_app,
    adapter: Ecto.Adapters.Postgres
end
