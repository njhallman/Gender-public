FROM dataeditors/stata18:2024-10-16

USER root
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    git-lfs \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-bibtex-extra \
    latexmk \
    biber \
    build-essential \
    pkg-config \
    libcairo2-dev \
    python3-dev \
    tmux \
    bash && \
    apt-get clean

# Set up proper shell environment
ENV SHELL=/bin/bash
ENV TERM=xterm-256color
RUN chsh -s /bin/bash statauser

# Upgrade pip and install newer meson & meson-python from PyPI
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install "meson>=1.0.0" meson-python

# Copy and install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Initialize Git LFS
RUN git lfs install

# Set up LaTeX environment
ENV PATH="/usr/local/texlive/2023/bin/x86_64-linux:$PATH"

# Ensure Stata license file permissions
RUN touch /usr/local/stata/stata.lic && \
    chmod 666 /usr/local/stata/stata.lic

# Ensure proper permissions for Stata
RUN chown -R statauser:stata /usr/local/stata && \
    chmod -R 755 /usr/local/stata

# Switch to Stata user
USER statauser

# Install Stata packages permanently
RUN echo "ssc install estout, replace" > /tmp/install.do && \
    echo "ssc install reghdfe, replace" >> /tmp/install.do && \
    echo "ssc install ftools, replace" >> /tmp/install.do && \
    /usr/local/stata/stata -b do /tmp/install.do && \
    rm /tmp/install.do