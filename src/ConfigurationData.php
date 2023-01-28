<?php

declare(strict_types=1);

namespace Neucore\Plugin\Mumble;
class ConfigurationData
{
    public function __construct(
        public array $groupsToTags,

        public ?int $bannedGroup,

        /**
         * @var array<array<string>>
         */
        public array $additionalTagGroups,
    ) {
    }
}
