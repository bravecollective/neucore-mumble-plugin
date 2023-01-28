<?php

declare(strict_types=1);

namespace Neucore\Plugin\Mumble;

class ConfigurationData
{
    public function __construct(
        public string $databaseEnvVar,

        public string $nickname,

        public array $groupsToTags,

        public bool $mainTagReplacesCorporationTicker,

        /**
         * @var array<array<string>>
         */
        public array $additionalTagGroups,

        public ?int $bannedGroup,
    ) {
    }
}
