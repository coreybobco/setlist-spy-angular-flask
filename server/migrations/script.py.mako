"""$***REMOVED***message***REMOVED***

Revision ID: $***REMOVED***up_revision***REMOVED***
Revises: $***REMOVED***down_revision | comma,n***REMOVED***
Create Date: $***REMOVED***create_date***REMOVED***

"""
from alembic import op
import sqlalchemy as sa
$***REMOVED***imports if imports else ""***REMOVED***

# revision identifiers, used by Alembic.
revision = $***REMOVED***repr(up_revision)***REMOVED***
down_revision = $***REMOVED***repr(down_revision)***REMOVED***
branch_labels = $***REMOVED***repr(branch_labels)***REMOVED***
depends_on = $***REMOVED***repr(depends_on)***REMOVED***


def upgrade():
    $***REMOVED***upgrades if upgrades else "pass"***REMOVED***


def downgrade():
    $***REMOVED***downgrades if downgrades else "pass"***REMOVED***
